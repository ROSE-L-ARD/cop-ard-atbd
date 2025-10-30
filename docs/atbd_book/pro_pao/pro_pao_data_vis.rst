.. _pro_pao_data_vis:

=====================
Data visualization
=====================

PRO /PAO products are stored in Zarr format and it is possible to load it directly in Jupyter notebooks or GIS environment (e.g. QGIS).

The products is stored in a *datatree* structure with main variables and metadata.

In the following a short guide to open the product and access variables and metadata is provided.


.. _open_pro_pao_datatree:

Opening PRO / PAO products in python
====================================

Overview
--------

`xarray.open_datatree` is a convenient function that allows opening hierarchical Zarr datasets as a tree of `xarray.Dataset` objects. This is particularly useful when working with Zarr stores containing multiple nested groups.

Prerequisites
-------------

- **xarray version**: 2024.11.0 or higher

Step-by-Step Instructions
-------------------------

.. code-block:: python

   import xarray as xr

   # Path to the Zarr store
   zarr_path = "/path/to/your/data.zarr"

   # Open the Zarr store as a DataTree
   offset = xr.open_datatree(zarr_path, engine="zarr", chunks={}, decode_coords='all')

Accessing Groups
''''''''''''''''

Each group in the Zarr hierarchy becomes a node in the `DataTree`.  

In order to display all the available groups it is sufficient to execute the following command:

.. code-block:: python

   offset.groups

It is possible to access a specific group using its path. For instance in order to access the measurement group in correspondence of the burst "iw1_202704" and return it as a dataset:

.. code-block:: python

   measuremnts = offset["/iw1_202704/measuremnts"].ds  # Returns an xarray.Dataset


Optional Arguments
''''''''''''''''''

It is possible to customize the behavior using optional parameters:

- ``decode_cf=True`` to apply CF conventions
- ``backend_kwargs={"consolidated": True}`` to read consolidated metadata

Notes
-----

- Zarr paths can be local or cloud-hosted.
- For cloud storage use URL and ensure authentication is configured.

See Also
--------

- `xarray DataTree documentation <https://xarray-datatree.readthedocs.io/>`__
- `Zarr Python library <https://zarr.readthedocs.io/>`__


.. _pro_pao_qgis_guide:

Loading PRO / PAO products in QGIS
==================================

Overview
--------

Zarr is a storage format for chunked, compressed, N-dimensional arrays.  
As of GDAL 3.4+, support for reading Zarr is integrated and available in QGIS builds that bundle an appropriate GDAL version.

This guide explains how to load Zarr data in QGIS as a raster layer.

Prerequisites
-------------

- **QGIS version**: 3.22 or higher (with GDAL ≥ 3.4)
- **Zarr dataset**: stored locally or accessible via a supported virtual file system (e.g., `/vsiaz/` for Azure)

Step-by-Step Instructions
-------------------------

1. **Check GDAL Version**

   In QGIS, go to:

   - ``Help → About → Providers``  
   - Confirm that the **GDAL version** is 3.4 or higher.

2. **Open the Data Source Manager**

   - Click on ``Layer → Add Layer → Add Raster Layer``  
   - Choose **File** as the source type.

3. **Specify the Zarr Dataset Path**

   Use the GDAL ZARR syntax in the file field:

   .. code-block:: text

      ZARR:"/path/to/your/data.zarr/"

   Replace the path with actual directory. Ensure it points to the root of the Zarr hierarchy.

4. **Add the Layer**

   - Click ``Add``.  
   - If the dataset is supported and properly georeferenced, it should load as a raster layer.

Cloud Storage Notes
-------------------

For cloud-hosted Zarr files (e.g., Azure Blob Storage), prepend the virtual file system path as needed:

.. code-block:: text

   /vsiaz/container/data.zarr/

It is necessary to configure environment with appropriate credentials or shared access signatures.

Limitations
-----------

- QGIS supports reading **single Zarr arrays** at a time.  
- Very large datasets or complex hierarchies may load slowly.  
- Metadata must conform to GDAL-readable NetCDF/Zarr conventions.

See Also
--------

- `GDAL Zarr driver documentation <https://gdal.org/drivers/raster/zarr.html>`__
- `QGIS raster data formats <https://docs.qgis.org/latest/en/docs/user_manual/working_with_raster/index.html>`__

