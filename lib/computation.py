import copy
import inspect
import itertools
import typing
from typing import Any, Callable, Dict, KeysView, List, Literal, Mapping, Sequence, Tuple, Union, ValuesView, cast

import dask.distributed
import numpy as np
import structlog
import xarray as xr

import lib.io

logger = structlog.get_logger(__name__)


class Client(object):
    def __init__(self, **kwargs):
        self.client = None
        self.client_options = kwargs

    def __enter__(self):
        self.client = create_client(**self.client_options)

    def __exit__(self, *args):
        if self.client is not None:
            destroy_client(self.client)


class DummyClient(object):
    def __init__(self):
        self.name = "dummy-client"

    def scatter(self, data, **kwargs):
        return data

    def compute(self, results):
        return [DummyFuture(e) for e in results]

    def cancel(self, *args, **kwargs):
        pass

    def restart(self, **kwargs):
        pass

    def map(self, func, *args, **kwargs):
        return [DummyFuture(func(*arg, **kwargs)) for arg in zip(*args)]

    def gather(self, results):
        return [e.result() for e in results]


class DummyFuture(object):
    def __init__(self, obj):
        self.name = "dummy-client"
        self._result = obj

    def result(self):
        return self._result


def conditional_delayed(enable_dask):
    def wrapper(func):
        if enable_dask:
            return dask.delayed(func)
        else:
            return func

    return wrapper


def optimize_chunks(data: xr.DataArray, chunks: dict) -> dict:
    """

    The objective of this optimization is to make output
    chunks lies on the same grid of the data chunking.
    When data is not chunked, chunks will not be changed

    """
    import copy

    chunks_opt = copy.deepcopy(chunks)
    i_valid = np.empty((0), dtype="int32")

    for k in chunks.keys():
        c = data.chunksizes.get(k, None)  # type: Union[np.typing.NDArray[Any], tuple[int, ...], None]
        if c is not None:
            c = np.asarray(c, dtype="int32")
            if any(c[:-1] - c[0] != 0):
                raise ValueError(
                    f"data dimension {k} has an irregular chunking that "
                    "is not compatible with the chunks optimization procedure",
                )
            else:
                v = np.array(chunks[k], dtype="int32")
                v_opt = (np.round(v / c[0]) * c[0]).astype("int32")
                v_opt[v == 0], v_opt[v == (data.sizes[k] - 1)] = 0, (data.sizes[k] - 1)

                chunks_opt[k] = v_opt
                i_valid = np.hstack((i_valid, np.where(v_opt.ptp(axis=1) != 0)[0]))

    i_valid = np.unique(i_valid)
    for k in chunks.keys():
        chunks_opt[k] = tuple(cast(List[Any], map(tuple, chunks_opt[k][i_valid, :])))
    return chunks_opt


def get_chunks(
    data: xr.DataArray,
    chunks: Dict[str, Tuple] | None = None,
    chunksizes: Dict[str, int] | None = None,
    chunking_optimization: bool = False,
) -> Tuple[Dict[str, Tuple], Dict[str, Any], int]:
    """

    Return optimized chunks for data. The objective of the chunks optimization
    is to make the output chunks lies on the same grid of the data chunking

    :param chunks: chunks to be used. It must have the following structure:
                    {dim_0: ((start_0, end_0), (start_1, end_1), ..., (start_n, end_n))
                    dim_1: ((start_0, end_0), (start_1, end_1), ..., (start_n, end_n))
                    ...
                    dim_m: ((start_0, end_0), (start_1, end_1), ..., (start_n, end_n))}
                    All the data dimensions must be contained into the chunks dictionary
    :param chunksizes: chunk sizes to be used to chunk data. It must have the following structure:
                       {dim_0: size_0, dim_1, size_1, ..., dim_m: size_m}
                       When some dimensions of data are not present in the chunksizes
                       dictionary, data will not chunk along those directions
    :param chunking_optimization: when it is true the chunking will be optimized by considering
                                  the data chunking. The objective of this optimization is to make
                                  the output chunks lies on the same grid of the data chunking

    The structure of the returned value will be the same of the chunks parameter

    """
    _chunks, _indices = {}, {}
    if chunks is None:
        if chunksizes is None:
            k: Union[str, KeysView[str]]
            v: Union[
                np.typing.NDArray[Any], Tuple[int, ...], List[int], Tuple[Tuple[int, int]], List[Tuple[Tuple[int, int]]]
            ]

            for k, v in data.chunksizes.items():
                v = np.insert(np.cumsum(v), 0, 0)
                if not (isinstance(k, str)):
                    raise Exception(f"Expected str, got {type(k)}")
                _chunks[k], _indices[k] = zip(*tuple(((v[i], v[i + 1]), i) for i in range(len(v) - 1)))
        else:
            if ((set(chunksizes.keys()) - set(cast(Tuple[str], data.dims))) == set()) is False:
                raise Exception(
                    f"chunksizes element list {tuple(chunksizes.keys())} must be a subset of the data\
                    dimension set {data.dims}",
                )
            for k in cast(Tuple[str], data.dims):
                if k in chunksizes:
                    if chunksizes[k] >= data[k].size:
                        logger.warning(
                            f"The chunksize for dimension {k} is larger than data size "
                            f"along with this dimension. In such a case for this dimension "
                            f"a single chunk of size {chunksizes[k]} will be used",
                        )
                        v = [0, chunksizes[k]]
                    else:
                        v = list(range(0, data[k].size, chunksizes[k])) + [data[k].size]
                    v, j = zip(*tuple(((v[i], v[i + 1]), i) for i in range(len(v) - 1)))
                else:
                    v, j = ((0, data[k].size),), (0,)
                _chunks[k], _indices[k] = v, j
        v = list(cast(tuple, zip(*itertools.product(*_chunks.values()))))
        _chunks = {k: v for k, v in zip(_chunks.keys(), v)}
        v = list(cast(tuple, zip(*itertools.product(*_indices.values()))))
        _indices = {k: v for k, v in zip(_indices.keys(), v)}
    else:
        k, v = chunks.keys(), cast(List[Tuple[Tuple[int, int]]], list(cast(ValuesView, chunks.values())))
        if (set(k) == set(data.dims)) is False:
            raise Exception("chunks must contain all the data dimensions")
        if (all(len(v[0]) == len(e) for e in v)) is False:
            raise Exception("the lists of values of chunks cannot have a different number of elements")
        if (all(i[0] <= i[1] for j in v for i in j)) is False:
            raise Exception("chunk start value must be lower than or equal to the corresponding end value")
        if (all(np.max(v) <= data[k].size for k, v in chunks.items())) is False:
            raise Exception("all chunks values must be lower than the size of the corresponding data dimension")
        _chunks = dict(chunks)
        _indices = {k: (0,) * len(v) for k, v in _chunks.items()}
    if chunking_optimization:
        _chunks = optimize_chunks(data, _chunks)
    return _chunks, _indices, len(list(_chunks.values())[0])


def apply_overlap(
    chunks: Dict[str, Tuple],
    overlap_sizes: Mapping[str, Any] = {},
) -> dict:

    _chunks_ov = {}
    for k in chunks.keys():
        delta = overlap_sizes[k] if k in overlap_sizes else 0
        _chunks_ov[k] = [[s - delta if s > delta else 0, e + delta] for (s, e) in chunks[k]]
    return _chunks_ov


def try_to_combine(
    results: List[xr.DataArray | xr.Dataset | str],
) -> List[xr.DataArray | xr.Dataset] | xr.DataArray | xr.Dataset | None:

    _results: list[Any] = []
    if len(results) == 0:
        return None

    def try_to_combine_(result):

        try:
            # when func returns paths, I will try  #
            # reading and then concatenating them  #
            if all(isinstance(e, str) for e in result) and all(s1_ard_core.computing.io.isdir(e) for e in result):
                _result = [s1_ard_core.computing.io.read(e) for e in result]
            else:
                raise ValueError("result does not seem to be data file")
        except (FileNotFoundError, ValueError):
            _result = result

        _dims, _ok = [list(e.dims) for e in _result], False
        if (len(_dims[0]) == 1) and all(e == _dims[0] for e in _dims):
            # in such a case there is only one dimension and it is the same for all the #
            # result elements so I can try to use concatenate along this dimension     #
            try:
                _result = xr.concat(_result, dim=_dims[0][0])
                _ok = True
            except:
                logger.warning("concat failed results will be returned as a list")
        else:
            # the last resource (I kwown!) is trying to use combine_by_coords
            try:
                _result = xr.combine_by_coords(_result)
                _ok = True
            except:
                logger.warning("conbine_by_coords failed results will be returned as a list")
        return _result if _ok else result

    result: Any  # mypy fix
    for result in zip(*results) if all(isinstance(e, (list, tuple)) for e in results) else (results,):
        _s = [getattr(e, "attrs", {}).get("store_path", None) for e in result]
        if (_s[0] is not None) and all(_s[0] == e for e in _s):
            # all the result elements have been saved into the same store_path. In such a case  #
            # case, results have been concatenated yet and I just have to return one of them    #
            result = result[0]
        else:
            if all(isinstance(e, (xr.DataArray, xr.Dataset, str)) for e in result):
                # when func returns a list of xr.DataArray or xr.Dataset I will try to concatenate them    #
                # On the contrary, when the output of the called function is not a xr.DataArray or a       #
                # xr.Dataset or a list of paths I simply return the list of the function output objects    #
                result = try_to_combine_(result)
        _results += (result,)
    return _results if len(_results) > 1 else _results[0]


def retrieve_client(
    client_options: dict = {},
    enable_dask: bool = True,
    **kwargs: dict,
) -> Tuple[Union[dask.distributed.Client, DummyClient], bool, bool, Union[bool, None], bool, int]:
    c_opt = copy.deepcopy(client_options)
    # client options retrieve #
    name = c_opt.pop("name", None)
    # name = c_opt.pop("name", "127.0.0.1:8786")
    c_type = c_opt.pop("type", "LOCAL")
    create = c_opt.pop("create", None)
    restart = c_opt.pop("restart", False)
    broadcast = c_opt.pop("broadcast", False)
    enable_dask &= c_type != "DUMMY"

    if enable_dask:
        jobs_chunksize = 20_000
        try:
            # client retrieve if dask is enabled #
            client: Union[DummyClient, dask.distributed.client.Client] = dask.distributed.get_client(name)
        except (ValueError, OSError):
            create = True
            logger.warning("No global client found a new one will be created")

        if create:
            n_jobs, job_memory = [c_opt.pop(e, None) for e in ["n_jobs", "job_memory"]]
            client = create_client(c_type, n_jobs, job_memory, **c_opt)
    else:
        jobs_chunksize = 1
        client = create_client("DUMMY")

    return client, enable_dask, restart, create, broadcast, jobs_chunksize


def select_scatter_strategy(
    objs: Sequence[xr.DataArray | xr.Dataset],
    scatter_strategy: str | None = None,
    memory_threshold: float = 512,
) -> Tuple[Union[None, str], bool]:
    """

    Select the optimal scattering strategy for the input objects

    :param objs: list of objects to be scattered on the cluster
    :param memory_threshold: expressed in MB
    :param scatter_strategy: the automatic strategy selection will be performed
                             only when scattering_strategy is not None
    """
    if scatter_strategy is None:
        to_m = 1024.0 * 1024
        v = [
            ((obj[dim].dtype.itemsize * obj[dim].size) / to_m) <= memory_threshold
            for obj in objs
            for dim in obj.dims
            if dim in obj.coords
        ]
        return ("once-and-for-all", True) if all(v) else ("inside-loop", False)
    else:
        return (scatter_strategy, scatter_strategy == "once-and-for-all")


@typing.no_type_check
def map_blocks(
    func: Callable[..., Any],
    obj: Union[Sequence[xr.DataArray | xr.Dataset], xr.Dataset, xr.DataArray],
    obj_ov: Sequence[xr.DataArray] = [],
    combine: bool = True,
    enable_dask: bool = True,
    chunks: dict | None = None,
    chunksizes: Mapping[str, Any] | None = None,
    chunking_optimization: bool = False,
    overlap_sizes: Mapping[str, Any] = {},
    fix_memory_leak: bool | Literal["auto"] = False,  # n_replicate: int = 0,
    scatter_strategy: Literal["once-and-for-all", "inside-loop", "no-scatter"] | None = None,
    resources: Mapping[str, Any] = {"cores": 1, "memory": 1024},  # memory in MB
    scheduler: str | None = "synchronous",
    client_options: Mapping[str, Any] = {},
    args: Sequence[Any] = (),
    kwargs: Mapping[str, Any] = {},
) -> List[Any] | xr.DataArray | xr.Dataset:
    """

    Apply a function to each block of the obj

    :param func: it is the function to be executed
    :param obj: it is a sequence of objects to processed
    :param obj_ov: it is a sequence of objects to processed with overlapped chunks
    :param enable_dask: when True tasks will be executed in parallel on a dask cluster.
                        On the contrary, tasks will not be submitted on a dask cluster and
                        they will be sequentially executed
    :param combine: when True I will try to combine the results obatained by the processing
                    of the single chunks. On the contrary, when set to False these results
                    will be returned as a simple list of objects
    :param chunks: chunks to be used. It must have the following structure:
                    {dim_0: ((start_0, end_0), (start_1, end_1), ..., (start_n, end_n))
                    dim_1: ((start_0, end_0), (start_1, end_1), ..., (start_n, end_n))
                    ...
                    dim_m: ((start_0, end_0), (start_1, end_1), ..., (start_n, end_n))}
                    All the data dimensions must be contained into the chunks dictionary
    :param chunksizes: chunk sizes to be used to chunk data. It must have the following structure:
                       {dim_0: size_0, dim_1, size_1, ..., dim_m: size_m}
                       When some dimensions of data are not present in the chunksizes
                       dictionary, data will not chunk along those directions
    :param overlap_sizes: overlap sizes to create the overlapped chunks when required
                          It must have the following structure: {dim_0: ov_0, dim_1, ov_1, ..., dim_m: ov_m}
                          The overlapped chunks will be used to chunk the elements of the obj_ov list and will
                          be computed as follows: chunks_ov[dim_0] = [chunk[dim_0] - ov_0, chunk[dim_0] + ov_0]
    :param fix_memory_leak: flag to try keeping workers memory under control. When True jobs will be aggregated
                            and executed as chunk of jobs, the client will be restarted at the end of the execution
                            of each job chunk. When False nothing changes: all the jobs will be (all toghether)
                            submitted to the scheduler. When 'auto' the submision behavior will depend on the
                            number of jobs to be executed (i.e. when the number of jobs is greater than five times
                            the job chunk size this flag will be set to True)
    :param resources: resources required to execute the tasks. It has to be a dict
                      that can contain any resource type dask allows to use.
                      (Default: {'cores': 1, 'memory': '1024'})
    :param scatter_strategy: data scattering strategy. When it is None the scattering strategy will be
                             automatically selected considering the actual data to be scattered on the cluster
    :param scheduler: scheduler to be used
    :param client_options: options for the client, so far the only actually used are:
                           name: used to retrieve the client object (Default: None)
                           create: when true a new client will be created by using
                                   type, n_jobs and job_memory if set
                           type: type of cluster to be created. This value is ignored when create
                                 is False or when enable_dask is False; in the latter case, type
                                 will be forced to DUMMY
                           n_jobs: number of jobs of the cluster that has to be created
                                   (ignored when create is False or when enable_dask is False)
                           job_memory: memory (e.g. "3.7GB") of each jobs of the cluster that is to
                                       be created (ignored when create is False or when enable_dask is False)
                           restart: when True the client will be restarted when the
                                    tasks are completed (Default: False)
                           broadcast: this boolean value will be used to set the broadcast parameter
                                      when obj and args are scattered over the cluster (Default: False)

                           In addition, any other parameter managed by the constructor of the selected client
                           object can be set as client_options. So far, the two available clients are:
                           - dask.distributed.LocalCluster (LOCAL)
                           - dask.dask_jobqueue.SLURMCluster (SLURM)

    """
    # client retrieve #
    client, enable_dask, restart, destroy, broadcast, jobs_chunksize = retrieve_client(
        client_options,
        enable_dask=enable_dask,
    )

    # function signature extraction #
    func_parameters = inspect.signature(func).parameters

    # input objs from now on must be lists or tuples  #
    # DO NOT MOVE THE FOLLOWING FOUR LINES FROM HERE  #
    _objs = [obj] if not isinstance(obj, (list, tuple)) else list(obj)
    _objs_ov = [obj_ov] if not isinstance(obj_ov, (list, tuple)) else list(obj_ov)
    _args = [args] if not isinstance(args, (list, tuple)) else list(args)
    i_ov = len(_objs) + 1

    # flag_ov = bool(_objs_ov)

    # optimal scattering strategy selection #
    scatter_strategy, apply_isel = select_scatter_strategy((_objs + _objs_ov), scatter_strategy)
    logger.debug(f"Selected scatter strategy: {scatter_strategy}")

    @conditional_delayed(enable_dask)
    def execute(objs, args, indices, block_id, job_id, apply_isel=apply_isel):
        # reserved keywords set #
        if "chunk" in func_parameters:
            kwargs["chunk"] = indices[0]
        if "chunk_ov" in func_parameters:
            kwargs["chunk_ov"] = indices[i_ov]

        if "job_id" in func_parameters:
            kwargs["job_id"] = job_id
        if "block_id" in func_parameters:
            kwargs["block_id"] = block_id

        # processing execution #
        if apply_isel is True:
            objs = [obj.isel(index) for (obj, index) in zip(objs, indices)]
        with dask.annotate(resources=resources), dask.config.set(scheduler=scheduler):
            res = func(*objs, *args, **kwargs)
        return res

    _chunks, _block_ids, _n_chunks = get_chunks(_objs[0], chunks, chunksizes, chunking_optimization)
    logger.debug(f"Number of blocks to be processed: {_n_chunks}")

    # when requested, the overlapped chunks will be computed #
    _chunks_ov = apply_overlap(_chunks, overlap_sizes)

    # submission behavior setting #
    if fix_memory_leak == "auto":
        fix_memory_leak = _n_chunks > jobs_chunksize

    # dask bug: a dict cannot be scattered #
    _future_args = [_arg if isinstance(_arg, dict) else client.scatter(_arg, broadcast=broadcast) for _arg in _args]
    if scatter_strategy == "no-scatter":
        _future_objs = _objs + _objs_ov
    elif scatter_strategy == "once-and-for-all":
        _future_objs = [client.scatter(_obj, broadcast=broadcast) for _obj in (_objs + _objs_ov)]

    results, job_array = [], []
    for j in range(_n_chunks):
        _block_id = {k: v[j] for k, v in _block_ids.items()}
        _chunk = {k: slice(v[j][0], v[j][1], None) for k, v in _chunks.items()}
        _chunk_ov = {k: slice(v[j][0], v[j][1], None) for k, v in _chunks_ov.items()}

        # chunk to slice indices #
        _i = [{k: v for k, v in _chunk.items() if k in _obj.dims} for _obj in _objs]
        _i += [{k: v for k, v in _chunk_ov.items() if k in _obj.dims} for _obj in _objs_ov]

        if scatter_strategy == "inside-loop":
            _objs_isel = [_obj.isel(index) for _obj, index in zip((_objs + _objs_ov), _i)]
            _future_objs = [client.scatter(_obj, broadcast=broadcast) for _obj in _objs_isel]
        job_array += [execute(_future_objs, _future_args, _i, _block_id, j)]
        if (j + 1) % jobs_chunksize == 0:
            if fix_memory_leak and enable_dask and (restart or destroy):
                results, job_array = results + [DummyFuture(e.result()) for e in client.compute(job_array)], []
                # client restart #
                client.restart()

                # if required data must be re-scattering on the new cluster #
                _future_args = [
                    _arg if isinstance(_arg, dict) else client.scatter(_arg, broadcast=broadcast) for _arg in _args
                ]
                if scatter_strategy == "once-and-for-all":
                    _future_objs = [client.scatter(_obj, broadcast=broadcast) for _obj in (_objs + _objs_ov)]
            else:
                results, job_array = results + client.compute(job_array), []

    if job_array:
        results += client.compute(job_array)
    results = [e.result() for e in results]  # if enable_dask else results

    if destroy:
        destroy_client(client)
    elif restart:
        client.restart()
    else:
        [client.cancel(e) for e in _future_args + _future_objs]

    return try_to_combine(results) if combine else results


def map(
    func: Callable[..., Any],
    args: Union[Sequence[List | Tuple], Tuple, List] = (),
    kwargs: Mapping[str, Any] = {},
    enable_dask: bool = True,
    combine: bool = True,
    resources: Mapping[str, Any] = {"cores": 1, "memory": 1024},  # memory in MB
    scheduler: str | None = "synchronous",
    client_options: dict = {},
) -> List[Any] | xr.DataArray | xr.Dataset | None:
    """

    Apply a function to each elemetns of the input lists

    :param func: it is the function to be executed
    :param args: list of arguments to be passed to func
                 if func has n mandatory input parameters
                 len(args) must be equal to n and all the args
                 elements (each one has to be a list or a tuple)
                 must have the same lenght
    :param client_options: options for the client, so far the only actually used are:
                           name: used to retrieve the client object (Default: None)

    """
    if (isinstance(args, (list, tuple))) is False:
        raise Exception("args must be a list or a tuple")
    _args = (args,) if not isinstance(args[0], (list, tuple, np.ndarray)) else args
    if (all(len(_args[0]) == len(e) for e in _args)) is False:
        raise Exception("args elements must have the same length")

    def execute(*args, **kwargs):
        with dask.annotate(resources=resources), dask.config.set(scheduler=scheduler):
            return func(*args, **kwargs)

    # client retrieve #
    client, enable_dask, restart, destroy, _, _ = retrieve_client(client_options, enable_dask=enable_dask)
    results = client.gather(client.map(execute, *_args, **kwargs))

    if destroy:
        destroy_client(client)
    elif restart:
        client.restart()

    return try_to_combine(results) if combine else results


def submit(
    func: Callable[..., Any],
    block: bool = False,
    args: Sequence[Any] = (),
    kwargs: Mapping[str, Any] = {},
    resources: Mapping[str, Any] = {"cores": 1, "memory": 1024},  # memory in MB
    scheduler: str | None = "synchronous",
    client_options: dict = {},
) -> List[Any] | xr.DataArray | xr.Dataset | None:

    # client retrieve #
    client, _, restart, destroy, broadcast, _ = retrieve_client(client_options)

    @dask.delayed
    def execute(args):
        with dask.annotate(resources=resources), dask.config.set(scheduler=scheduler):
            res = func(*args, **kwargs)
        return res

    _future_args = [
        _arg if isinstance(_arg, dict) else client.scatter(_arg, broadcast=broadcast)
        for _arg in ([args] if not isinstance(args, (list, tuple)) else list(args))
    ]
    job = client.compute(execute(_future_args))
    if block is True:
        result = job.result()

        if destroy:
            destroy_client(client)
        elif restart:
            client.restart()

    return result


def create_cluster(
    type: Literal["LOCAL", "SLURM", "DUMMY"] = "LOCAL",
    n_jobs: int | None = None,
    job_memory: Union[str, int] | None = None,
    **kwargs: Any,
):
    """

    Create client (LOCAL, SLURM and DUMMY types are allowed)

    """
    import psutil

    if (type in ["LOCAL", "SLURM", "DUMMY"]) is False:
        raise Exception("Invalid cluster type. Allowed types are LOCAL, SLURM and DUMMY")

    # get the number of logical cores and RAM memory
    if n_jobs is None:
        n_jobs = psutil.cpu_count()
    if job_memory is None:
        job_memory = int(psutil.virtual_memory().total / n_jobs * 0.95)
        if kwargs.get("processes", True) is False:
            job_memory *= n_jobs

    logger.debug(f"<Cluster info: type={type}, " f"n_jobs={n_jobs}, job_memory={job_memory}>")
    if type == "SLURM":
        import dask_jobqueue

        cluster = dask_jobqueue.SLURMCluster(
            queue=kwargs.pop("queue", "LocalQ"),
            account=kwargs.pop("account", "user"),
            cores=kwargs.pop("cores", 1),
            memory=job_memory,
            processes=1,
            walltime=kwargs.pop("walltime", "48:00:00"),
            **kwargs,
        )  # type: Union[dask_jobqueue.SLURMCluster,dask.distributed.LocalCluster,str]
        if isinstance(cluster, dask_jobqueue.SLURMCluster):
            cluster.scale(jobs=n_jobs)
    elif type == "LOCAL":
        cluster = dask.distributed.LocalCluster(
            n_workers=n_jobs,
            memory_limit=job_memory,
            processes=kwargs.pop("processes", True),
            threads_per_worker=kwargs.pop("threads_per_worker", 1),
            **kwargs,
        )
    elif type == "DUMMY":
        cluster = "DUMMY"

    return cluster


def create_client(
    type: Literal["LOCAL", "SLURM", "DUMMY"] = "LOCAL",
    n_jobs: int | None = None,
    job_memory: str | None = None,
    **kwargs: dict,
) -> dask.distributed.client.Client | DummyClient:
    """

    Create client (LOCAL, SLURM and DUMMY types are allowed)

    """
    if (type in ["LOCAL", "SLURM", "DUMMY"]) is False:
        raise Exception("Invalid cluster type. Allowed types are LOCAL, SLURM and DUMMY")

    cluster = create_cluster(type, n_jobs, job_memory, **kwargs)

    return DummyClient() if cluster == "DUMMY" else dask.distributed.Client(cluster)


def destroy_client(
    client: dask.distributed.client.Client,
):
    """

    Destroy the client

    """
    if isinstance(client, dask.distributed.client.Client):
        try:
            client.cluster.close(timeout=30)
            client.close(timeout=30)
        except dask.distributed.TimeoutError:
            logger.warning("Unable to gracefully destroy the client")
    elif isinstance(client, DummyClient):
        pass
    del client
