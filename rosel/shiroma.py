# Copyright 2024 European Union
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Dict, Mapping, cast
import warnings
import dask.array as da
import numpy as np
import scipy
import xarray as xr

import rosel.computation
import rosel.io

warnings.filterwarnings("ignore")


def compute_chunks(chunks: dict, overlap: dict) -> Dict:
    """
    Compute overlapped chunks to use in rosel.computation.map_blocks.

    Args:
        chunks (dict): Dictionary of simulation chunks
        overlap (dict): Dictionary defining the overlap between chunks
        dim_x_global (int): geogrid size along the x-axis.
        dim_y_global (int): geogrid size along the y-axis.

    Returns:
        chunks (Dict): dictionary containing overlapped chunks
    """
    if (overlap["x"] < chunks["x"][0]) is False:
        raise Exception(f"Overlap {overlap['x']} is bigger than chunk length {chunks['x'][0]}")
    if (overlap["y"] < chunks["y"][0]) is False:
        raise Exception(f"Overlap {overlap['y']} is bigger than chunk length {chunks['y'][0]}")

    dx = 1 if chunks["x"][-1] == 1 else 0
    dy = 1 if chunks["y"][-1] == 1 else 0

    for k in chunks.keys():
        delta = overlap[k] if k in overlap else 0
        aa = []
        if k == "x" or k == "y":
            for en, i in enumerate(chunks[k]):
                if en == 0:
                    s = 0
                    e = i + delta
                elif en == len(chunks[k]) - 1:
                    if chunks[k][-1] == 1:
                        break
                    else:
                        s = e - delta
                        e = s + chunks[k][-1]
                else:
                    s = e - delta
                    e = s + i + delta
                aa.append([s, e])
        if k == "y":
            y = np.repeat(aa, len(chunks["x"]) - dx, axis=0).tolist()
        elif k == "x":
            x = np.tile(aa, (len(chunks["y"]) - dy, 1)).tolist()
        else:
            axis = np.tile([0, 3], ((len(chunks["y"]) - dy) * (len(chunks["x"]) - dx), 1)).tolist()

    return {"y": y, "x": x, "axis": axis}


def flatten_radar_image(
    slc: xr.DataArray,
    A: xr.DataArray,
    data_path: str,
    data_name: str = "flattened_intensity",
    read: bool = False,
):
    chunk_size = slc.slant_range_time.size * slc.chunksizes["azimuth_time"][0]
    slc_flat = (
        (slc.drop_vars(slc.coords).squeeze())
        .stack(radar=["azimuth_time", "slant_range_time"])
        .reset_index("radar")
        .drop_vars(["azimuth_time", "slant_range_time"])
    ).chunk(radar=chunk_size)

    A_flat = A.chunk(radar=chunk_size)

    c = slc_flat / np.sqrt(A_flat)
    rosel.io.write(c, rosel.io.normpath(f"{data_path}/{data_name}"))
    return c if read else None


def map_geo_ap(
    c_path: str,
    simulation: xr.DataArray,
    data_path: str,
    data_name: str = "geo_ap",
    multilook: Dict[str, int] = {"azimuth_time": 1, "slant_range_time": 1},
    enable_dask: bool = True,
    read: bool = False,
    scheduler: str = "synchronous",
    client_options: Mapping[str, Any] = {},
) -> xr.DataArray | None:
    """
    Compute the geocoded values for each pixel in the geogrid.

    Args:
        c_path (str): Path to the flattened radar image.
        simulation (xr.DataArray): The radar data simulation.
        data_path (str): Path to the directory where results will be saved.
        data_name (str): Name of the zarr directory to store the result. Defaults to "geo_ap".
        multilook (Dict or None, optional): Defaults to {"azimuth_time": 1, "slant_range_time": 1}.
        enable_dask (bool or None, optional): Whether to enable Dask for parallel computation. Defaults to True.
        read (bool or None, optional): Whether to read the computed results back into memory after computation.
        Defaults to False.
        resources (Mapping[str, Any], optional): Resources available for the computation.
        Defaults to {"cores": 1, "memory": 1024}.
        scheduler (str or None, optional): Dask scheduler to use. Defaults to "synchronous".

    Returns:
        g (xr.DataArray | None): The geocoded values for each pixel in the geogrid  (if 'read' is True).
    """
    if not ((len(multilook) == 2) & all(i in ["azimuth_time", "slant_range_time"] for i in multilook.keys())):
        raise Exception(f"Expected dictionary with keys azimuth_time and slant_range_time. Got {multilook}")
    global_values = rosel.io.read(data_path=rosel.io.normpath(f"{data_path}/global_values"))
    dim_x_global = int(global_values.geo_xsize.values)
    dim_y_global = int(global_values.geo_ysize.values)
    bbox = global_values.bbox.values
    # chunk_length has to be the same chunk_length used in map_w
    chunk_length = int(global_values.chunk_length.values)
    if chunk_length != dict(simulation.chunksizes)["x"][0]:
        raise Exception(
            f'Got different chunk length. Simulation {dict(simulation.chunksizes)["x"][0]}, chunk length {chunk_length}'
        )

    g_global = xr.Dataset(
        data_vars={
            "v": (
                ["y", "x"],
                da.empty(
                    shape=(dim_y_global, dim_x_global),
                    chunks=(chunk_length, chunk_length),
                    dtype=complex,
                ),
            )
        }
    )
    g_global = g_global.assign_coords({"y": simulation.y[0:-1].values, "x": simulation.x[0:-1].values})
    rosel.io.write(
        g_global,
        data_path=rosel.io.normpath(f"{data_path}/{data_name}"),
        compute=False,
        skip_read=True,
        fill_value=0.0,
    )

    # compute chunks
    overlap = {"axis": 0, "y": 1, "x": 1}
    chunks = compute_chunks(dict(simulation.chunksizes), overlap)

    args = [c_path, chunk_length, dim_x_global, data_path, data_name, bbox, multilook]

    rosel.computation.map_blocks(
        func=compute_geo_ap,
        obj=simulation,
        args=args,
        chunks=chunks,
        enable_dask=enable_dask,
        scheduler=scheduler,
        client_options=client_options,
    )

    return rosel.io.read(rosel.io.normpath(f"{data_path}/{data_name}"), mask_and_scale=False).v if read else None


def compute_geo_ap(
    simulation: xr.DataArray,
    c_path: str,
    chunk_length: int,
    dim_x_global: int,
    data_path: str,
    data_name: str,
    bbox: np.ndarray,
    multilook: Dict[str, int],
    job_id=None,
) -> None:
    """
    Compute the geocoded values for each pixel in the geogrid within the current nlook block.

    Args:
        nlook (xr.DataArray): The computed 'nlook' dataset.
        c (xr.DataArray): The flattened radar image.
        chunk_length (int): Size of a chunk.
        dim_x_global (int): Geogrid size along the x-axis.
        data_path (str): Path to the directory where results will be saved.
        job_id (int): Identifier for the job.

    Returns:
        None: This function saves the computed geocoded values directly to the disk and does not return any data.
    """
    dim_x = simulation.x.size - 1
    dim_y = simulation.y.size - 1

    # create region
    row_number = job_id // (np.ceil(dim_x_global / chunk_length).astype(int))
    column_number = job_id % (np.ceil(dim_x_global / chunk_length).astype(int))
    region = {
        "y": slice(row_number * chunk_length, row_number * chunk_length + dim_y),
        "x": slice(column_number * chunk_length, column_number * chunk_length + dim_x),
    }

    # load corresponding weights
    if rosel.io.exists(path=rosel.io.normpath(f"{data_path}/w/{job_id}.npz")):
        with rosel.io.open(path=rosel.io.normpath(f"{data_path}/w/{job_id}.npz"), mode="rb") as f:
            w = scipy.sparse.load_npz(f)
    else:
        w = scipy.sparse.csr_array((1, 1))

    if w.nnz != 0:
        w = (w / w.sum(axis=1)[:, np.newaxis]).tocsr()
        radar_min = np.min(w.indices)
        radar_max = np.max(w.indices)
        if (multilook["azimuth_time"] == 1) & (multilook["slant_range_time"] == 1):
            c = (
                rosel.io.read(c_path, consolidate_metadata=False, mask_and_scale=False)
                .isel(radar=slice(radar_min, radar_max + 1))
                .values
            )
            g = xr.DataArray((w[:, radar_min : radar_max + 1] @ c).reshape(dim_y, 4 * dim_x), dims=["y", "x"])
        else:

            dr = 0 if bbox[2] % multilook["slant_range_time"] == 0 else 1
            da = 0 if bbox[3] % multilook["azimuth_time"] == 0 else 1
            rg_size = bbox[2] // multilook["slant_range_time"] + dr
            az_size = bbox[3] // multilook["azimuth_time"] + da

            radar_coords = np.unique(w.indices)
            col = (radar_coords % bbox[2]) // multilook["slant_range_time"]
            row = (radar_coords // bbox[2]) // multilook["azimuth_time"]
            col_multilook = row * rg_size + col
            data = np.ones_like(col_multilook)
            T = scipy.sparse.csr_array((data, (radar_coords, col_multilook)), shape=(w.shape[1], rg_size * az_size))
            T_min = np.min(T.indices)
            T_max = np.max(T.indices)
            c = (
                rosel.io.read(c_path, consolidate_metadata=False, mask_and_scale=False)
                .isel(radar=slice(T_min, T_max + 1))
                .values
            )
            g = xr.DataArray(
                (w[:, radar_min : radar_max + 1] @ T[radar_min : radar_max + 1, T_min : T_max + 1] @ c).reshape(
                    dim_y, 4 * dim_x
                ),
                dims=["y", "x"],
            )

        g = g.coarsen(x=4).sum().astype(complex)  # type: ignore
        rosel.io.write(
            g.drop_vars(g.coords),
            data_path=rosel.io.normpath(f"{data_path}/{data_name}"),
            region=region,
            consolidated=False,
            mode="r+",
            skip_read=True,
        )
    return
