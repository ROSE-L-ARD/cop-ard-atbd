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

Let :math:`(x,y)` be the coordinates of each point in the reference image, the offsets to be applied to obtain the corresponding coordinates in the secondary image is obtained combining the model-based offset :math:`(\Delta t_{r_s}, \Delta t_{a_s})` and the data-driven residual offsets :math:`(\hat{\delta} t_{r_s}, \hat{\delta} t_{a_s})` as follows:

.. math::
    :label: eq_rubber_sheeting
    
    \Delta_{corr} t_{r_s}(x,y) = \Delta t_{r_s}(x,y) + \hat{\delta} t_{r_s}(x,y)

    \Delta_{corr} t_{a_s}(x,y) = \Delta t_{a_s}(x,y) + \hat{\delta} t_{a_s}(x,y)

The residual offsets :math:`(\hat{\delta} t_{r_s}, \hat{\delta} t_{a_s})` are reconstructed over the reference image grid using an interpolator starting from the sparse set of residual offsets estimated at the patches or burst barycenters.

If the expected error arises from global effects such as orbital data inaccuracies, this reconstruction can be achieved by fitting a polynomial function of the desired order (e.g., a simple constant is generally sufficient for ESD).  

In general, to compensate for ionospheric effects or where a polynomial function is insufficient to capture the offset variability across the image, an interpolator with a regularization factor must be adopted, to ensure that the interpolated values are smooth and continuous across the image.

.. note::
    A robust estimation technique must be employed to remain insensitive to outliers.
    For instance, outliers can be identified by comparing the values at a given patch with the median of the neighboring patches and discarding them if the difference exceeds a certain threshold. The removed outliers can then be replaced with the corresponding median values.

Detailed variable description
-----------------------------

.. list-table:: Variable Description Table
   :widths: 25 50
   :header-rows: 1

   * - Symbol
     - :math:`\Delta t_{r_s}`
   * - Description
     - Residual offsets in slant range direction, to be applied to the secondary image to match the reference image, computed using the model-based methods
   * - Purpose
     - Input
   * - Units
     - seconds
   * - Type
     - float
   * - Dimensionality
     - (range, azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`\Delta t_{a_s}`
   * - Description
     - Residual offsets in azimuth direction, to be applied to the secondary image to match the reference image, computed using the model-based methods
   * - Purpose
     - Input
   * - Units
     - nanoseconds
   * - Type
     - timedelta64[ns]
   * - Dimensionality
     - (range, azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`\delta t_{r_s}`
   * - Description
     - Residual offsets in slant range direction, to be applied to the secondary image to match the reference image, computed using image matching or ESD
   * - Purpose
     - Input
   * - Units
     - seconds
   * - Type
     - float
   * - Dimensionality
     - (range, azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`\delta t_{a_s}`
   * - Description
     - Residual offsets in azimuth direction, to be applied to the secondary image to match the reference image, computed using image matching or ESD
   * - Purpose
     - Input
   * - Units
     - nanoseconds
   * - Type
     - timedelta64[ns]
   * - Dimensionality
     - (range, azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`\hat{\delta} t_{r_s}`
   * - Description
     - Residual offsets in slant range direction, to be applied to the secondary image to match the reference image, reconstructed over the reference image through interpolation
   * - Purpose
     - Internal
   * - Units
     - seconds
   * - Type
     - float
   * - Dimensionality
     - (range, azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`\hat{\delta} t_{a_s}`
   * - Description
     - Residual offsets in azimuth direction, to be applied to the secondary image to match the reference image, reconstructed over the reference image through interpolation
   * - Purpose
     - Internal
   * - Units
     - nanoseconds
   * - Type
     - timedelta64[ns]
   * - Dimensionality
     - (range, azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`\Delta_{corr} t_{r_s}`
   * - Description
     - Corrected offset in slant range direction to be applied to the secondary image to match the reference image
   * - Purpose
     - Input
   * - Units
     - seconds
   * - Type
     - float
   * - Dimensionality
     - (range, azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`\Delta_{corr} t_{a_s}`
   * - Description
     - Corrected offset in azimuth direction to be applied to the secondary image to match the reference image
   * - Purpose
     - Input
   * - Units
     - nanoseconds
   * - Type
     - timedelta64[ns]
   * - Dimensionality
     - (range, azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -