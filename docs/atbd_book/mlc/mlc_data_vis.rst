.. _mlc_data_vis:

=====================
Data visualization
=====================

Interferogram generation in GIS software
--------------------------------------------

It is possible to generate interferograms directly in a GIS software. Once the zarr file is loaded, one needs only calling a "raster calculator" function operating on two chosen dates. 
For example in QGIS on can pick two rasters that correspond to the chose dates and take the phase difference

.. math::
    \phi = \phi_1 - \phi_2

and feed it to a function that realizes the two-argument arctangent by using only the common arctangent, sine, and cosine:

.. math::
    \varphi = \mathrm{atan2}\left(\sin(\phi), \cos(\phi)\right) = 2\:\mathrm{atan}\left(\frac{\sin(\phi)}{1+\cos(\phi)}\right)= 2\:\mathrm{atan}\left(\frac{1- \cos(\phi)}{\sin(\phi)}\right).

