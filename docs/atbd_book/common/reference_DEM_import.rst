.. _reference_DEM_import:

DEM Import
''''''''''''''''

Overview
--------
The objective of *dem_import* is to retrieve the Digital Elevation Model over the area covered by the input SLC data.  
The input DEM can be read directly from `Copernicus DEM portal <https://data.earthdatahub.destine.eu/copernicus-dem/GLO-30-v0.zarr>`_, or passed as an external file.  
This function provides the DEM as is, on the original grid.

Input
------

The *DEM import* tool requires the following inputs:

- :math:`slcs`: Sentinel-1 Level 1 SLC product. This is a mandatory input. The unit will extract the bounding box from this product to define the area of interest for the DEM import.

Output
------

The *DEM import* tool provides as output the :math:`DEM` as is in the original reference system and spacing.

Processing parameters
---------------------

dem_type:  
    Type of DEM to be imported. It can be either a georeferenced file or "Copernicus". 
    If "Copernicus" is selected, the DEM will be downloaded from the Copernicus DEM portal.  

border:  
   Margin to be applied when extracting the bounding box of the input SLC product, to define the area of interest for the DEM import.


Algorithm
---------

The *dem_import* reads the DEM from exteral georeferenced file or directly from `Copernicus DEM portal <https://data.earthdatahub.destine.eu/copernicus-dem/GLO-30-v0.zarr>`_.  
The area of interest is defined by the bounding box of the input *slcs* product.  
For efficiency reasons, it is important to maintain the chunking of the input DEM, particularly when accessing the DEM remotely.
