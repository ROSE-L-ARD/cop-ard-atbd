import os
import pathlib
import shutil
import typing
import uuid
from typing import Any, List, Literal, Mapping, Tuple, Union

import datatree
import fsspec
import numpy as np
import retry
import s3fs
import xarray as xr
import zarr


# @timeit
@retry.retry(tries=3, delay=5)
def write(
    data: xr.Dataset | xr.DataArray | datatree.DataTree,
    data_path: str | None = None,
    root: str | None = None,
    region: Mapping[str, slice] | None = None,
    keep_attrs: bool = False,
    group: str | None = None,
    consolidated: bool = True,
    mode: str = "w",
    compute: bool = True,
    skip_read: bool = False,
    fill_value=None,
    **kwargs,
) -> Union[datatree.DataTree, xr.Dataset, xr.DataArray, None]:
    """

    Writes the input data as a zarr store

    :params data: input data to be saved
    :params root: root path of the zarr store
    :params data_path: zarr store name, if it is None
                       an uuid will be used as file name

    """
    mode = mode if region is None else "r+"
    if any(e is not None for e in [root, data_path]) is False:
        raise Exception("At least one between root and data_path must be set")
    if ((data_path is not None) and (root is not None)) is True:
        raise Exception("Just one between data_path and root can be set")
    if isinstance(data, (xr.DataArray, xr.Dataset, datatree.DataTree, xr.core.datatree.DataTree)) is False:
        raise Exception(f"Data type must be either a xr.Dataset or a xr.DataArray. Received {type(data).__name__}")
    if isinstance(data, datatree.DataTree) and group is not None:
        AssertionError("group must be None if type(data) == datatree.Datatree")

    if group is not None:
        kwargs["group"] = group = group.lstrip("/")
    _file_path = data_path if data_path is not None else str(uuid.uuid4())
    if root is not None:
        _file_path = os.path.join(root, _file_path)

    # path normalization #
    _file_path = normpath(_file_path)
    _data_attrs = {"store_path": _file_path}
    _data: Union[xr.Dataset, xr.core.datatree.DataTree, datatree.DataTree]
    if isinstance(data, xr.DataArray):
        _data = data.to_dataset(name="v")
        _data_attrs["obj_type"] = "xr.DataArray"
    elif isinstance(data, (datatree.DataTree, xr.core.datatree.DataTree)):
        _data = data
        _data_attrs["obj_type"] = "datatree.Datatree"
    else:
        _data = data
        _data_attrs["obj_type"] = "xr.Dataset"

    # encoding reset DO NOT MOVE FROM HERE
    if hasattr(_data, "drop_encoding"):
        _data = _data.drop_encoding()
    elif hasattr(_data, "reset_encoding"):
        _data = _data.reset_encoding()
    elif isinstance(_data, (datatree.DataTree, xr.core.datatree.DataTree)):
        for node in _data.descendants:
            for v in node.ds.variables.values():
                v.encoding = {}

    as_type = _data_attrs["obj_type"]
    if isinstance(_data, xr.Dataset) and (group is not None):
        _data = datatree.DataTree.from_dict({group: _data})
        _data_attrs["obj_type"] = "datatree.Datatree"
        del kwargs["group"]

    # to keep all existing attributes #
    if mode in ["a", "a-", "r+"] and keep_attrs:
        _data_attrs = {**getattr(read(_file_path, group, as_type=as_type), "attrs", {}), **_data_attrs}
    if region is None:
        # patch to manage timedelta64 and deltatime64 #
        encoding = {
            name: {"chunks": tuple(chunk[0] for chunk in var.chunks)}
            for name, var in _data.variables.items()
            if var.chunks
        }
        if fill_value is not None:
            for name, var in _data.data_vars.items():
                encoding[name]["_FillValue"] = fill_value
    else:
        encoding = None
        # drop all dimension coordinates to avoid concurrent writing
        _data = _data.drop_vars(set(_data.dims).intersection(set(_data.coords)))

    try:
        _data = _data.assign_attrs(_data_attrs)
    except AttributeError:
        for k, v in _data_attrs.items():
            _data.attrs[k] = v
    _data.to_zarr(  # type: ignore
        _file_path, mode=mode, region=region, compute=compute, consolidated=consolidated, encoding=encoding, **kwargs
    )

    return read(_file_path, group, as_type=as_type) if skip_read is False else None


def read(
    data_path: str,
    group: str | None = None,
    as_type: str | None = None,
    invalidate_cache: bool = True,
    consolidate_metadata: bool = True,
    **kwargs,
) -> xr.DataArray | xr.Dataset | datatree.DataTree:
    """

    Try to read a xr.DataArray, xr.Dataset or datatree.Datatree

    :param data_path: path to the zarr to be read
    :param group: when datapath contains a datatree the group
                  to be read can be specified
    :param invalidate_cache: when True the cache will be cleaned
    :param consolidate_metadata: when True the zarr metadata will be
                                 consolidate before read the store

    """
    if consolidate_metadata:
        zarr.consolidate_metadata(data_path)
    if invalidate_cache:
        fsspec.filesystem("s3").invalidate_cache()

    def to_dataarray(ds):
        if len(ds.data_vars) == 1:
            return ds[list(ds.data_vars)[0]]
        raise ValueError(f"cannot cast {data_path} to xr.DataArray")

    _data: Union[datatree.DataTree, xr.Dataset, xr.DataArray] = datatree.open_datatree(
        data_path, engine="zarr", chunks={}, mode="r", **kwargs
    )
    data_attrs = _data.attrs
    if data_attrs.get("obj_type", as_type) == "xr.DataArray":
        _data = to_dataarray(_data.to_dataset())
    elif data_attrs.get("obj_type", as_type) == "xr.Dataset":
        _data = _data.to_dataset()
    elif group is not None:
        _data = _data[group]
        data_path = os.path.join(data_path, group)
        if as_type == "xr.Dataset":
            _data = _data.to_dataset()
        elif as_type == "xr.DataArray":
            _data = to_dataarray(_data.to_dataset())

    for k, v in data_attrs.items():
        if k in ["obj_type", "store_path"]:
            _data.attrs[k] = v

    if as_type is not None:
        _data.attrs["obj_type"] = as_type
    _data.attrs["store_path"] = data_path

    return _data


def read_chunks(data_path: str) -> Mapping[str, tuple]:
    """

    Returns a dictionary with chunking of each variable,
    dimension and coordinate of the zarr store

    """
    z = zarr.open_group(data_path, mode="r")
    return {k: z[k].chunks for k in z.array_keys()}


def read_shape(data_path: str) -> Mapping[str, tuple]:
    """

    Returns a dictionary with shape of each variable,
    dimension and coordinate of the zarr store

    """
    z = zarr.open_group(data_path, mode="r")
    return {k: z[k].shape for k in z.array_keys()}


def update_attrs(
    attrs: Mapping[str, Any],
    data_path: str,
    group: str | None = None,
):

    data = zarr.open_group(data_path)
    if group is not None:
        data = data[group]

    for k in attrs.keys():
        data.attrs.pop(k, None)

    data.attrs.update(attrs)


class Path(str):
    def __init__(self, path: str | pathlib.Path):
        if isinstance(path, pathlib.Path):
            path = path.as_posix()
        self._key = None
        self._bucket = None
        self._path = normpath(path)
        self._name = os.path.basename(path)
        self._stem = pathlib.Path(self._path).stem
        self._directory = os.path.dirname(path)
        if is_s3_path(path):
            self._bucket = path.split("/")[2]
            self._key = "/".join(path.split("/")[3:])

    def __str__(self) -> str:
        return self._path

    def __repr__(self) -> str:
        return self._path.__repr__()

    @classmethod
    def glob(cls, pattern: str, sort: bool = True):
        """

        Return a list of Path object one for each
        file really discovered by using glob

        """
        return [cls(e) for e in glob(pattern, sort=sort)]

    @property
    def name(self):
        return self._name

    @property
    def key(self):
        return self._key

    @property
    def bucket(self):
        return self._bucket

    @property
    def stem(self):
        return self._stem

    @property
    def directory(self):
        return self._directory

    def join(self, dir):
        """

        Append the directory to the path by using os.path.join

        """
        return Path(os.path.join(dir, self._path))

    def as_gdal(self):
        """

        Return a string that can be used to remote access from gdal

        """
        return f"/vsis3/{self._path[5:]}" if is_s3_path(self._path) else self._path

    def replace_dir(self, dir):
        """

        Return a new path with the same name and dir as directory. It
        does not move or copy anything; it just changes the path string

        """
        return Path(os.path.join(dir, self._name))

    def copy(self, dst, recursive=False, only_if_different_fs=False):
        """

        Copy file into the destination

        TODO Improve management of case dst is a directory

        """
        _dst = self.replace_dir(dst) if isdir(dst) or dst.endswith("/") else dst
        return Path(copy(self._path, _dst, recursive=recursive, only_if_different_fs=only_if_different_fs))

    def move(self, dst, recursive=False, only_if_different_fs=False):
        """

        Move file into the destination path

        TODO Improve management of case dst is a directory

        """
        _dst = self.replace_dir(dst) if isdir(dst) or dst.endswith("/") else dst
        return Path(move(self._path, _dst, recursive=recursive, only_if_different_fs=only_if_different_fs))

    def exists(self):
        return exists(self._path)

    def isdir(self):
        return isdir(self._path)

    def isfile(self):
        return isfile(self._path)


def decorator(func):
    import inspect

    def wrapper(path: Union[list, tuple, str], **kwargs):
        _path = path[0] if isinstance(path, (list, tuple)) else path
        fs, _ = fsspec.core.url_to_fs(_path)

        # when S3 invalidate cache forces fetching the listing again #
        if hasattr(fs, "invalidate_cache"):
            fs.invalidate_cache()

        # Function dependent path pre-processing
        if func.__name__ == "delete" and kwargs.get("allow_non_existent"):
            path = (path,) if isinstance(path, str) else path
            path = [e for e in path if exists(e)]
            if len(path) == 0:
                return

        _func = getattr(fs, func.__name__)
        _kwargs = {k: v for k, v in kwargs.items() if k in inspect.signature(_func).parameters}
        res = _func(path, **_kwargs)

        # Function dependent result post-processing
        if func.__name__ == "glob":
            if not isinstance(path, str):
                raise Exception(f"Expected str, got {type(path)}")
            if path.startswith("s3://"):
                res = [f"s3://{e}" for e in res]
            if kwargs.get("sort", False):
                res = sorted(res)
        return res

    wrapper.__doc__ = getattr(fsspec.filesystem("file"), func.__name__).__doc__
    wrapper.__name__ = func.__name__
    return wrapper


@decorator
def exists(
    pathname: str,
):
    pass


@decorator
def isdir(
    pathname: str,
):
    pass


@decorator
def isfile(
    pathname: str,
):
    pass


@decorator
def touch(
    pathname: str,
):
    pass


@decorator
def delete(
    pathname: str,
    recursive=False,
    maxdepth=None,
    allow_non_existent=False,
):
    pass


@decorator
def makedirs(pathname: str, exist_ok: bool = False):
    pass


@decorator
def glob(pattern: str, sort: bool = False):
    pass


@decorator
def open(
    pathname: str,
    mode: str = "rb",
):
    pass


def normpath(
    pathname: str,
) -> str:
    """

    Normalize pathname, eliminating double slashes, etc

    """
    if pathname.startswith("s3://"):
        ret = f"s3://{os.path.normpath(pathname[5:])}"
    else:
        ret = os.path.normpath(pathname)
    return ret


def dirname(
    pathname: str,
) -> str:
    """

    Returns the path dirname

    """
    return os.path.dirname(normpath(pathname))


def is_s3_path(
    pathname: str,
) -> bool:
    fs, _ = fsspec.core.url_to_fs(pathname)
    return isinstance(fs, s3fs.core.S3FileSystem)


def _fop(
    function_name: Literal["move", "copy"],
    src: str,
    dst: str,
    recursive: bool = False,
    only_if_different_fs: bool = False,
) -> str:

    src_flag, dst_flag = [is_s3_path(e) for e in [src, dst]]

    if (src_flag == dst_flag) and (not only_if_different_fs):
        fs, _ = fsspec.core.url_to_fs(src)
        f = getattr(fs, function_name)
        f(src, dst, recursive=recursive)
    elif src_flag and (not dst_flag):
        fs = fsspec.filesystem("s3")
        fs.download(src, dst, recursive=recursive)
    elif (not src_flag) and (dst_flag):
        fs = fsspec.filesystem("s3")
        fs.upload(src, dst, recursive=recursive)
    else:
        dst = src
    return dst


def copy(
    src: str,
    dst: str,
    recursive: bool = False,
    only_if_different_fs: bool = False,
) -> str:
    """

    Copy src to dst src and dst can be both local and remote (S3) data

    :param src: soruce data path
    :param dst: destination data path
    :param recursive: when True if src is a directory
                      all the content will be trasferred
    :param only_if_different_fs: when True src data will be copied only if src and
                                 dst are not on the same filesystem

    """
    return _fop("copy", src, dst, recursive, only_if_different_fs)


def move(
    src: str,
    dst: str,
    recursive: bool = False,
    only_if_different_fs: bool = False,
) -> str:
    """

    Move src to dst src and dst can be both local and remote (S3) data
    when src or dst is a remote (S3) path the src file will be copied

    :param src: soruce data path
    :param dst: destination data path
    :param recursive: when True if src is a directory
                      all the content will be trasferred
    :param only_if_different_fs: when True src data will be moved only if src
                                 and dst are not on the same filesystem

    """
    result = _fop("move", src, dst, recursive, only_if_different_fs)
    if not is_s3_path(src) and exists(src):
        shutil.rmtree(src) if isdir(src) else os.remove(src)
    return result


# From here function to create output products


class MetadataTemplate:
    def __init__(self, template):
        """
        Initialize with a template dictionary where each key maps to a tuple:
        (type, default_value). If default_value is None, the parameter is required.
        """
        self.template = template

    def render(self, **kwargs):
        """
        Render the template by applying input data provided as keyword arguments.
        Attempt to cast input values to the expected type.
        Raise an error if a required key is missing or casting fails.
        """
        rendered = {}
        for key, (expected_type, default_value) in self.template.items():
            if key in kwargs:
                value = kwargs[key]
                try:
                    # Attempt to cast the value to the expected type
                    cast_value = expected_type(value)
                except (ValueError, TypeError) as e:
                    raise TypeError(f"Key '{key}' expects type {expected_type}, but casting failed: {e}")
                rendered[key] = cast_value
            elif default_value is not None:
                # Use default value if provided
                rendered[key] = default_value
            else:
                # Raise an error if the key is required but not provided
                raise ValueError(f"Key '{key}' is required but not provided.")
        return rendered


def read_datatree_node(data: datatree.DataTree, node_path: str, as_dataset: bool = True):
    node: Union[datatree.DataTree, xr.DataArray, xr.Dataset] = data
    for tag in node_path.split("/"):
        if tag in node.keys():
            node = node[tag]
        else:
            return datatree.DataTree.from_dict({})
    if as_dataset:
        node = node.to_dataset()
    return node.copy()
