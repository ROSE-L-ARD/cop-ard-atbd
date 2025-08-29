import structlog
import numpy as np
import xarray as xr
import numba as nb
from typing import Tuple, Dict, Any

import scipy
import scipy.sparse
import sparse

import ortools.graph.python.min_cost_flow
from functools import wraps
import time as tt

import ctypes as cty

logger = structlog.get_logger(__name__)

MAXJUMP = 1_000
MAXCOST = 1_000


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = tt.perf_counter()
        result = func(*args, **kwargs)
        end_time = tt.perf_counter()
        total_time = end_time - start_time
        logger.info(f"Function {func.__name__} Took {total_time:.4f} seconds")
        return result

    return timeit_wrapper


def wrap(v: np.ndarray, w: float = 2 * np.pi):
    w_ = w / 2.0
    return ((v + w_) % w) - w_


def unique(e: np.ndarray, return_index: bool = False) -> np.ndarray:
    """

    Return the unique edges and if requested
    (return_index == True) the indices of the
    unique elements

    """
    n_points = e.max() + 1
    i_type = "uint32" if (n_points**2) < np.iinfo("uint32").max else "uint64"
    i_unique = e.min(axis=1).astype(i_type) * n_points + e.max(axis=1).astype(i_type)
    _, i_unique = np.unique(i_unique, return_index=True)
    r = (e[i_unique, :], i_unique) if return_index else e[i_unique, :]

    return r


def get_edges(
    xx: np.ndarray,
    yy: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:

    # Dealunay triangulation
    triangle = scipy.spatial.Delaunay(np.vstack((xx, yy)).T)

    # modifica triangoli adiacenti
    triang = np.copy(triangle.simplices)
    neigh = np.copy(triangle.neighbors)

    # archi senza massa
    e_ = np.vstack(
        (np.roll(triang, -1, axis=1).flatten(), np.roll(triang, -2, axis=1).flatten())
    ).T

    # identify border triangles / arcs
    border = triangle.neighbors == -1

    # add inverted border arcs
    e = np.vstack((e_, np.roll(e_[border.flatten(), :], -1, axis=1)))

    # return arcs without repetition, arcs with repetition, neighbours
    return (unique(np.vstack(e)), e, neigh)


def get_dual_graph_(
    neigh: np.ndarray,
    n_vertices: int = 3,
    maxcost: int = MAXCOST,
    maxjump: int = MAXJUMP,
    cost_mask: np.ndarray | None = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:

    # check borders
    border = neigh == -1
    n_border = border.sum()
    neigh_ = np.copy(neigh)
    if n_border:
        neigh_[border] = neigh.max() + 1

    n_triang = neigh.shape[0]
    n_edges = neigh.size + n_border

    # set costs
    scale = maxcost * np.ones(n_edges)
    if cost_mask is not None:
        scale = scale * cost_mask
    cost = np.round(scale).astype(cty.c_int32)

    # set maximum arc capacity
    ucap = (np.ones(n_edges) * maxjump).astype(cty.c_int32)

    # dual graph (offset 1 fortran style)
    head_2 = (
        np.repeat(np.arange(n_triang)[:, None], n_vertices, axis=1).flatten() + 1
    ).astype(cty.c_int32)
    tail_2 = (neigh_.flatten() + 1).astype(cty.c_int32)

    if n_border > 0:
        # add earth node
        triang_border, _ = np.where(border)
        head_2 = np.hstack((head_2, np.zeros(n_border) + neigh_.max() + 1)).astype(
            cty.c_int32
        )
        tail_2 = np.hstack((tail_2, triang_border + 1)).astype(cty.c_int32)

    return head_2, tail_2, cost, ucap


@timeit
def integ_mcf_ortools(
    start_nodes: np.ndarray,
    end_nodes: np.ndarray,
    supplies: np.ndarray,
    unit_costs: np.ndarray,
    capacities: np.ndarray,
):

    smcf = ortools.graph.python.min_cost_flow.SimpleMinCostFlow()

    # Add arcs, capacities and costs in bulk using numpy.
    all_arcs = smcf.add_arcs_with_capacity_and_unit_cost(
        start_nodes, end_nodes, capacities, unit_costs
    )

    # Add supply for each nodes.
    smcf.set_nodes_supplies(np.arange(0, len(supplies)), supplies)

    # Find the min cost flow.
    status = smcf.solve()

    if status != smcf.OPTIMAL:
        logger.debug("There was an issue with the min cost flow input.")
        logger.debug(f"Status: {status}")
        logger.debug(
            f"start_nodes: {start_nodes.min()} {start_nodes.max()} {start_nodes.shape}"
        )
        logger.debug(
            f"end_nodes: {end_nodes.min()} {end_nodes.max()} {end_nodes.shape}"
        )
        logger.debug(
            f"unit_costs: {unit_costs.min()} {unit_costs.max()}  {unit_costs.shape}"
        )
        logger.debug(
            f"capacities: {capacities.min()} {capacities.max()} {capacities.shape}"
        )
        logger.debug(f"supplies: {supplies.min()} {supplies.max()} {supplies.shape}")

        raise Exception

    solution_flows = smcf.flows(all_arcs)

    return (0, solution_flows)


@nb.jit(nopython=True)
def depth_first_order_sum(prec, nodes, grad):
    # init solution
    sol = np.zeros(nodes.max() + 1)

    # integration
    for i, j, g in zip(prec, nodes, grad):
        sol[j] = sol[i] + g

    return sol


@timeit
def integ_tree(grad: sparse.COO, es: np.ndarray) -> np.ndarray:
    """Integration exploiting the tree structure of the graph"""

    # integration exploiting depth_first_order
    gg = scipy.sparse.csr_matrix(
        (np.ones(es.shape[0]), (es[:, 0], es[:, 1])), shape=grad.shape
    )
    nodes, prec = scipy.sparse.csgraph.depth_first_order(gg, es.min())

    p = prec[nodes[1:]]  # parent
    n = nodes[1:]  # nodes
    g = np.array(grad[p, n], dtype=float).squeeze()  # gradients

    # integration
    sol = depth_first_order_sum(p, n, g)

    # return solution
    return sol


def apply_corr(
    e: np.ndarray, g: np.ndarray, n_points: int, flow: np.ndarray, **kwargs
) -> sparse.COO:
    # original gradients
    # e_ = e.copy() #compute() if isinstance(e, da.Array) else e
    # _, ind = np.unique(e_[:, 0]*(n_points+1) + e_[:, 1], return_index=True)
    # e_ = e_[ind, :]

    grad = sparse.COO((e[:, 0], e[:, 1]), g, shape=(n_points, n_points)).tocsr()

    # corrected gradients
    grad[e[:, 1], e[:, 0]] += flow
    grad[e[:, 0], e[:, 1]] -= flow

    return grad


@timeit
def get_dual_graph(
    e: np.ndarray,
    es: np.ndarray,
    neigh: np.ndarray,
    w: np.ndarray,
    n_points: int,
    solver: Dict[str, Any],
):
    # get dual graph

    # check params
    maxjump = solver["maxjump"] if "maxjump" in solver.keys() else MAXJUMP
    maxcost = solver["maxcost"] if "maxcost" in solver.keys() else MAXCOST

    weight = scipy.sparse.lil_matrix((n_points, n_points), dtype="float32")
    weight[e[:, 0], e[:, 1]] = w
    weight[e[:, 1], e[:, 0]] = w
    weight = weight.tocsr()
    w_ = np.array(weight[es[:, 0], es[:, 1]]).squeeze()

    # return head_2, tail_2, cost, ucap
    return get_dual_graph_(neigh, maxcost=maxcost, cost_mask=w_, maxjump=maxjump)


@timeit
def solve(
    e: np.ndarray,
    es: np.ndarray,
    g: np.ndarray,
    w: np.ndarray,
    neigh: np.ndarray,
    solver: Dict[str, Any],
) -> Tuple[int, float, np.ndarray]:

    n_points = e.max() + 1
    scale_demand = solver["scale_demand"] if "scale_demand" in solver.keys() else 1.0

    # compute graph size
    n_vertices = neigh.shape[1]

    # duplicate gradients
    grad = scipy.sparse.lil_matrix((n_points, n_points), dtype="float32")
    grad[e[:, 0], e[:, 1]] = g
    grad[e[:, 1], e[:, 0]] = -g
    # grad = grad.tocsr()

    # extract duplicate edges
    g_ = np.array((grad.tocsr())[es[:, 0], es[:, 1]]).squeeze()

    # get dual graph
    head_2, tail_2, cost, ucap = get_dual_graph(e, es, neigh, w, n_points, solver)

    # compute demand
    demand = np.round(g_[: neigh.size].reshape(-1, n_vertices).sum(axis=1)).astype(
        cty.c_int32
    )

    # add earth node (if needed)
    earth = -demand.sum()
    if earth != 0:
        demand = np.hstack((demand, earth)).astype(cty.c_int32)

    # update cost if requested
    if scale_demand is not None:
        imax = demand.size * n_vertices
        weight = scipy.sparse.lil_matrix((n_points, n_points), dtype="float32")
        # scale according to the demands
        weight[es[:imax, 0], es[:imax, 1]] = (
            1.0
            / np.repeat(
                1.0 + scale_demand * np.abs(demand)[:, None], n_vertices, axis=1
            ).flatten()
        )
        weight = weight.tocsr()
        # make scaling weigth symmetric
        weight = np.sqrt(weight * weight.T)
        # apply scaling
        cost[:imax] = (
            cost[:imax] * np.array(weight[es[:imax, 0], es[:imax, 1]]).squeeze()
        )
        # cost[:imax] = cost[:imax] / np.repeat(1 + np.abs(demand)[:, None], n_vertices, axis=1).flatten()

    exit_status, flow = integ_mcf_ortools(head_2 - 1, tail_2 - 1, demand, cost, ucap)

    if exit_status != 0:
        logger.error(f"Unable to solve MCF exit code {exit_status}")

    # apply corrections
    grad[es[:, 1], es[:, 0]] += flow
    grad[es[:, 0], es[:, 1]] -= flow

    # integration on minimum spanning tree
    sol = integ_tree(grad.tocsr(), es)

    return exit_status, flow.sum(), sol


def integ_mcf(
    xx: np.ndarray,
    yy: np.ndarray,
    ph: np.ndarray,
    cohe: np.ndarray,
    solver: Dict[str, Any],
) -> Tuple[int, float, np.ndarray]:
    """
    Integrate the gradients using a minimum cost flow algorithm.

    Parameters:
    - xx: x-coordinates of the points
    - yy: y-coordinates of the points
    - ph: wrapped phase values
    - w: weights for the edges
    - solver: dictionary with solver parameters
    - kwargs: additional parameters

    Returns:
    - exit_status: exit status of the solver
    - total_cost: total cost of the solution
    - sol: integrated solution
    """

    # get edges and neighbors
    e, es, neigh = get_edges(xx, yy)

    # gradients extraction and normalization
    g = wrap(ph[e[:, 1]] - ph[e[:, 0]]) / (2 * np.pi)

    # weight computation in correspondence of edges
    w = cohe[e[:, 1]] * cohe[e[:, 0]]

    # solve MCF
    exit_status, total_cost, sol = solve(e, es, g, w, neigh, solver)
    sol = 2 * np.pi * sol

    return exit_status, total_cost, sol
