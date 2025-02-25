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

import warnings
from typing import Any, Dict, Mapping, cast

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


def apply_flattening(slc: xr.DataArray, A: xr.DataArray, eps: float, data_path: str, chunk=None) -> None:
    """
    Compute the flattened intensity of the radar image for each pixel in the region associated with
    the argument 'chunk'.

    Args:
        c (xr.DataArray): The radar image for each radar-grid pixel.
        A (xr.DataArray): The accumulated gamma-naught area for each radar-grid pixel.
        eps (float): Sets to 0 the values of A lower than eps.
        data_path (str): The path to the directory where the flattened radar image is stored.
        chunk (dict):  The chunk associated with the job.

    Returns:
        None: This function saves the flattened radar image directly to the disk and
              does not return any data.
    """

    mask = A > eps
    c = (cast(xr.DataArray, slc.drop_vars(slc.coords).squeeze())) / np.sqrt(A)
    c = c.where(mask, 0).astype("complex64")
    rosel.io.write(
        c,
        data_path,
        region=chunk,
        consolidated=False,
        mode="r+",
        skip_read=True,
    )
    return


def flatten_radar_image(
    slc: xr.DataArray,
    A: xr.DataArray,
    data_path: str,
    eps: float = 1e-3,
    multilook: Dict[str, int] = {"azimuth_time": 1, "slant_range_time": 1},
    enable_dask: bool = True,
    read: bool = False,
    resources: Mapping[str, Any] = {"cores": 1, "memory": 1024},
    scheduler: str = "synchronous",
    client_options: Mapping[str, Any] = {},
) -> xr.Dataset | None:
    """
    Compute the flattened intensity of the radar image for each radar-grid pixel.

    Args:
        slc (xr.DataArray): The intensity of the radar image for each radar-grid pixel.
        A (xr.DataArray): The accumulated gamma-naught area for each radar-grid pixel.
        data_path (str): The path to the directory where the flattened intensity is stored.
        eps (float, optional): Sets to 0 the values of A lower than eps. Defaults to 1e-3.
        enable_dask (bool, optional): Whether to enable Dask for parallel computation. Defaults to True.
        read (bool, optional): Whether to read the computed results back into memory after computation.
                               Defaults to False.
        resources (Mapping[str, Any], optional): Resources available for the computation.
                                                 Defaults to {"cores": 1, "memory": 1024}.
        scheduler (str or None, optional): Dask scheduler to use. Defaults to "synchronous".
        client_options (Mapping[str, Any], optional): Options for the Dask client, if using Dask.
                                                      Defaults to an empty dictionary.

    Returns:
       xr.DataArray or None: The flattened intensity of the radar image for each radar-grid pixel (if 'read' is True).
    """
    if not (set(multilook) == {"azimuth_time", "slant_range_time"}):
        raise Exception(f"Expected dictionary with keys azimuth_time and slant_range_time. Got {multilook}")

    if not ((multilook["azimuth_time"] == 1) & (multilook["slant_range_time"] == 1)):
        A = (
            A.coarsen(
                azimuth_time=multilook["azimuth_time"],
                slant_range_time=multilook["slant_range_time"],
                boundary="pad",
            )
            .mean()
            .chunk({i: slc.chunksizes[i][0] for i in slc.dims})
        )

    if not (slc.shape == A.shape):
        raise Exception(f"Expected same shape for slc and A. Got slc.shape {slc.shape}, A.shape {A.shape}")
    c = xr.Dataset(
        data_vars={
            "v": (
                ["azimuth_time", "slant_range_time"],
                da.empty(
                    shape=(slc.azimuth_time.size, slc.slant_range_time.size),
                    chunks=(slc.chunksizes["azimuth_time"][0], slc.chunksizes["slant_range_time"][0]),
                    dtype="complex64",
                ),
            )
        }
    )

    rosel.io.write(
        c,
        data_path=rosel.io.normpath(data_path),
        compute=False,
        skip_read=True,
        fill_value=0.0,
        mode="w",
    )
    args = [eps, rosel.io.normpath(data_path)]
    rosel.computation.map_blocks(
        apply_flattening,
        obj=(slc, A),
        args=args,
        enable_dask=enable_dask,
        resources=resources,
        scheduler=scheduler,
        client_options=client_options,
    )
    return rosel.io.read(rosel.io.normpath(data_path), mask_and_scale=False).v if read else None


def map_geo_ap(
    c_path: str,
    simulation: xr.DataArray,
    data_path_shiroma: str,
    data_path_geo_ap: str,
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
        data_path_shiroma (str): Path to the directory where the weights and global values are stored.
        data_path_geo_ap (str): Path to the directory where the geocoded values will be saved.
        multilook (Dict, optional): Defaults to {"azimuth_time": 1, "slant_range_time": 1}.
        enable_dask (bool, optional): Whether to enable Dask for parallel computation. Defaults to True.
        read (bool, optional): Whether to read the computed results back into memory after computation.
                               Defaults to False.
        resources (Mapping[str, Any], optional): Resources available for the computation.
        Defaults to {"cores": 1, "memory": 1024}.
        scheduler (str or None, optional): Dask scheduler to use. Defaults to "synchronous".
        enable_dask (bool, optional): Whether to enable Dask for parallel computation. Defaults to True.
        resources (Mapping[str, Any], optional): Resources available for the computation.
                                                 Defaults to {"cores": 1, "memory": 1024}.
        scheduler (str or None, optional): Dask scheduler to use. Defaults to "synchronous".
        client_options (Mapping[str, Any], optional): Options for the Dask client, if using Dask.
                                                      Defaults to an empty dictionary.
    Returns:
        xr.DataArray | None: The geocoded values for each pixel in the geogrid  (if 'read' is True).
    """
    if not (set(multilook) == {"azimuth_time", "slant_range_time"}):
        raise Exception(f"Expected dictionary with keys azimuth_time and slant_range_time. Got {multilook}")
    global_values = rosel.io.read(data_path=rosel.io.normpath(f"{data_path_shiroma}/global_values"))
    dim_x_global = int(global_values.geo_xsize.values)
    dim_y_global = int(global_values.geo_ysize.values)
    bbox = global_values.bbox.values
    # chunk_length has to be the same chunk_length used in map_w
    chunk_length = int(global_values.chunk_length.values)
    if chunk_length != dict(simulation.chunksizes)["x"][0]:
        raise Exception(
            f'Got different chunk length. Simulation {dict(simulation.chunksizes)["x"][0]}, chunk length {chunk_length}'
        )

    x = (simulation.x[0:-1].values + simulation.x[1:].values) / 2
    y = (simulation.y[0:-1].values + simulation.y[1:].values) / 2

    g_global = xr.Dataset(
        data_vars={
            "v": (
                ["y", "x"],
                da.empty(shape=(dim_y_global, dim_x_global), chunks=(chunk_length, chunk_length), dtype="complex64"),
            )
        },
        coords={"y": y, "x": x},
    )
    rosel.io.write(
        g_global,
        data_path=rosel.io.normpath(data_path_geo_ap),
        compute=False,
        skip_read=True,
        fill_value=0.0,
    )

    # compute chunks
    overlap = {"axis": 0, "y": 1, "x": 1}
    chunks = compute_chunks(dict(simulation.chunksizes), overlap)

    args = [c_path, chunk_length, dim_x_global, data_path_shiroma, data_path_geo_ap, bbox, multilook]
    rosel.computation.map_blocks(
        func=compute_geo_ap,
        obj=simulation,
        args=args,
        chunks=chunks,
        enable_dask=enable_dask,
        scheduler=scheduler,
        client_options=client_options,
    )

    return rosel.io.read(rosel.io.normpath(data_path_geo_ap), mask_and_scale=False).v if read else None


def compute_geo_ap(
    simulation: xr.DataArray,
    c_path: str,
    chunk_length: int,
    dim_x_global: int,
    data_path_shiroma: str,
    data_path_geo_ap: str,
    bbox: np.ndarray,
    multilook: Dict[str, int],
    job_id=None,
) -> None:
    """
    Compute the geocoded values for each pixel in the geogrid within the current nlook block.

    Args:
        simulation (xr.DataArray): The radar data simulation.
        c_path (str): Path to the flattened intensity of the radar image.
        chunk_length (int): Size of a chunk.
        dim_x_global (int): Geogrid size along the x-axis.
        bbox (np.ndarray): Bounding box coordinates ([0, 0, slc.slant_range_time.size, slc.azimuth_time.size])
                           defining the region of interest.
        data_path_shiroma (str): Path to the directory where the weights and global values are stored.
        data_path_geo_ap (str): Path to the directory where the geocoded values will be saved.
        multilook (Dict): ...
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
    if rosel.io.exists(path=rosel.io.normpath(f"{data_path_shiroma}/w/{row_number}.{column_number}.npz")):
        with rosel.io.open(
            path=rosel.io.normpath(f"{data_path_shiroma}/w/{row_number}.{column_number}.npz"), mode="rb"
        ) as f:
            w = scipy.sparse.load_npz(f)
    else:
        w = scipy.sparse.csr_array((1, 1))

    if w.nnz != 0:
        w = (w / w.sum(axis=1)[:, np.newaxis]).tocsr()
        radar_min = np.min(w.indices)
        radar_max = np.max(w.indices)

        if (multilook["azimuth_time"] == 1) & (multilook["slant_range_time"] == 1):
            y1 = radar_min // bbox[2]
            y2 = radar_max // bbox[2] + 1

            translated_radar_min = radar_min - y1 * bbox[2]
            translated_radar_max = radar_max - y1 * bbox[2]
            c = (
                rosel.io.read(c_path, consolidate_metadata=False, mask_and_scale=False)
                .isel(azimuth_time=slice(y1, y2))
                .v.values.ravel()[translated_radar_min : translated_radar_max + 1]
            )
            g = xr.DataArray((w[:, radar_min : radar_max + 1] @ c).reshape(dim_y, 4 * dim_x), dims=["y", "x"])
        else:
            dr = 0 if bbox[2] % multilook["slant_range_time"] == 0 else 1
            da = 0 if bbox[3] % multilook["azimuth_time"] == 0 else 1
            rg_size = bbox[2] // multilook["slant_range_time"] + dr
            az_size = bbox[3] // multilook["azimuth_time"] + da
            radar_coords = np.unique(w.indices)
            col = ((radar_coords % bbox[2]) // multilook["slant_range_time"]).astype("int32")
            row = (radar_coords // bbox[2]) // multilook["azimuth_time"]
            col_multilook = (row * rg_size + col).astype("int32")
            data = np.ones_like(col_multilook, dtype=bool)
            radar_coords = radar_coords - radar_min
            T = scipy.sparse.csr_array(
                (data, (radar_coords, col_multilook)), shape=(radar_max - radar_min + 1, rg_size * az_size)
            )
            T_min = np.min(T.indices)
            T_max = np.max(T.indices)
            y1 = T_min // rg_size
            y2 = T_max // rg_size + 1

            translated_radar_min = T_min - y1 * rg_size
            translated_radar_max = T_max - y1 * rg_size
            c = (
                rosel.io.read(c_path, consolidate_metadata=False, mask_and_scale=False)
                .isel(azimuth_time=slice(y1, y2))
                .v.values.ravel()[translated_radar_min : translated_radar_max + 1]
            )
            g = xr.DataArray(
                (w[:, radar_min : radar_max + 1] @ T[:, T_min : T_max + 1] @ c).reshape(dim_y, 4 * dim_x),
                dims=["y", "x"],
            )

        g = (g.coarsen(x=4).sum() / 2.0).astype("complex64")  # type: ignore
        rosel.io.write(
            g.drop_vars(g.coords),
            data_path=rosel.io.normpath(data_path_geo_ap),
            region=region,
            consolidated=False,
            mode="r+",
            skip_read=True,
        )
    return
