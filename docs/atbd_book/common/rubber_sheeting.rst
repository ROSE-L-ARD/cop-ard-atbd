.. _rubber_sheeting:

Rubber sheeting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Overview
--------

The purpose of this utility is to merge the offset between the reference and secondary images, estimated using both model-based and data-driven approaches.  
The offsets estimated with the model-based approach are already available on the reference radar grid and have been applied to pre-coregister the input images.  
The offsets estimated with the data-driven approach are available at a sparse set of points, corresponding either to the image patches used in image matching or to the barycenters of the overlapping areas between bursts (in the case of ESD).

Inputs
-------

- :math:`(\delta t_{r_s}, \delta t_{a_s})`: residual offsets in slant range and azimuth directions, to be applied to the secondary image to match the reference image; computed using image matching or ESD.  
- :math:`(\Delta t_{r_s}, \Delta t_{a_s})`: secondary disparity map on the reference grid, computed using the model-based method

Outputs
--------

- :math:`(\Delta_{corr} t_{r_s}, \Delta_{corr} t_{a_s})`: corrected offsets in azimuth and slant range directions to be applied to the secondary image to match the reference image

Algorithm
----------

The residual offsets are estimated at a set of patches in the case of image matching, or at burst overlap areas in the case of the ESD estimator.  
Starting from this sparse set of residual corrections, relative to the offsets estimated by the model, it is necessary to reconstruct the values over the reference image grid.

If the expected error arises from global effects such as orbital data inaccuracies, this reconstruction can be achieved by fitting a polynomial function of the desired order (e.g., a simple constant is generally sufficient for ESD).  

In general, to compensate for ionospheric effects or where a polynomial function is insufficient to capture the offset variability across the image, an interpolator with a regularization factor must be adopted.

.. note::
    A robust estimation technique must be employed to remain insensitive to outliers.
    For instance, outliers can be identified by comparing the values at a given patch with the median of the neighboring patches and discarding them if the difference exceeds a certain threshold. The removed outliers can then be replaced with the corresponding median values.
