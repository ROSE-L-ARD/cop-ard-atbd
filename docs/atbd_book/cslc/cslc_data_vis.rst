.. _cslc_data_vis:

=====================
Data visualization
=====================

Basic reading and selection operations
--------------------------------------------

The CSLC products is stored in a Zarr file with the azimuth and slant range coordinates expressed in time. It is possible to perform spatial, polarization or acquisition date selections.

.. code-block:: python
    :caption: Import modules

    # import basic modules
    import xarray
    import numpy as np
    import xrft

.. code-block:: python
    :caption: Data path definition & parameters

    data_path = # local path or s3 url

.. code-block:: python
    :caption: open cslc product and visualize data structure

    cslc = xr.open_datatree(data_path, engine='zarr', chunks={}, decode_coords='all)
    cslc.groups

.. code-block:: python
    :caption: open cslc product

    cslc_sel = 


, selections of the elements of the Once the Zarr file is loaded the extraction of the amplitude is very It is possible to generate interferograms directly in a GIS software. Once the zarr file is loaded, one needs only calling a "raster calculator" function operating on two chosen dates. 
For example in QGIS on can pick two rasters that correspond to the chose dates and take the phase difference

.. math::
    \phi = \phi_1 - \phi_2

and feed it to a function that realizes the two-argument arctangent by using only the common arctangent, sine, and cosine:

.. math::
    \varphi = \mathrm{atan2}\left(\sin(\phi), \cos(\phi)\right) = 2\:\mathrm{atan}\left(\frac{\sin(\phi)}{1+\cos(\phi)}\right)= 2\:\mathrm{atan}\left(\frac{1- \cos(\phi)}{\sin(\phi)}\right).

Interferogram generation
--------------------------------------------
