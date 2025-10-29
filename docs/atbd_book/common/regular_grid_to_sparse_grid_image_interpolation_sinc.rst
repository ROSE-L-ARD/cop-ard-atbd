.. _regular_grid_to_sparse_grid_image_interpolation_sinc:

Regular grid to sparse grid image interpolation - *image resampling*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Overview
--------
This function allows interpolation of a regular gridded image onto a sparse grid using the truncated *sinc* interpolation method. This is useful when resampling the secondary SLC image onto the same grid as the input reference image. In the case of complex images, it is assumed that the image is in baseband, meaning the phase has been appropriately deramped.
To limit the ripple effect caused by the finite length of the interpolator, a weighting function is applied using a bi-parametric Kaiser window.

Inputs
------
The tool requires the following inputs:

- :math:`SLC_{deramp}`: Deramped SLC image  
- :math:`(t_{r_r},t_{a_r})`: Output reference grid  
- :math:`(\Delta t_{r_s},\Delta t_{a_s})`: Secondary disparity map corresponding to the reference grid  

Outputs
-------
The tool provides the following output:

- :math:`CSLC_{deramp}`: Deramped coregistered SLC data  

Processing parameters
---------------------
The tool requires the following processing parameters:

- :math:`(S_{r},S_{a})`: Kernel size  
- :math:`\beta_{kaiser}`: Kaiser window shape parameter 

Algorithm
---------
The slant range :math:`\Delta t_{r_s}` and azimuth :math:`\Delta t_{a_s}` offsets in the secondary image, corresponding to the reference grid, are generally spatially variant, meaning the interpolation kernel varies point by point. The interpolation kernel is based on a windowed :math:`sinc()` interpolator. Ideally, the resampling could be performed independently for each pixel of the output image. It is assumed that the secondary image is already in baseband (i.e., deramping has been applied).  

Let :math:`(S_{r},S_{a})` be the size of the interpolation kernel, with :math:`K_{r}` defined as :math:`\{-S_{r}/2,...,S_{r}/2\}` and :math:`K_{a}` as :math:`\{-S_{a}/2,...,S_{a}/2\}`. The logical steps performed for each output pixel :math:`(t_{r_r},t_{a_r})` are:

1. Identification of the coordinates in the secondary image corresponding to the reference grid:

.. math::
    :label: coreg_abs_coord

    (t_{r_s},t_{a_s}) = (t_{r_r},t_{a_r})+(\Delta t_{r_s},\Delta t_{a_s})

2. Computation of the integer and fractional components of the coordinates in the secondary image (see the end of the paragraph for details):

.. math::
    :label: coreg_int_offset

    (\hat{t}_{r_s},\hat{t}_{a_s}) = round((t_{r_s},t_{a_s}))

.. math::
    :label: coreg_frac_offset

    (\delta t_{r_s},\delta t_{a_s}) = (t_{r_s},t_{a_s}) - (\hat{t}_{r_s},\hat{t}_{a_s})

3. Computation of the kernel based on the fractional offset:

.. math::
    :label: coreg_kernel_1

    k_x(x) = sinc(x + \delta t_{r_s}) * w_{kaiser}(x + \delta t_{r_s}, \beta=\beta_{kaiser}), \quad \forall \ x \in K_r

.. math::
    :label: coreg_kernel_2

    k_y(y) = sinc(y + \delta t_{a_s}) * w_{kaiser}(y + \delta t_{a_s}, \beta=\beta_{kaiser}), \quad \forall \ y \in K_a

.. math::
    :label: coreg_kernel_3

    k(x,y) = k_x^T(x,y) * k_y(x,y)

4. Application of the kernel:

.. math::
    :label: coreg_kernel_apply

    CSLC_{deramp}(t_{r_r},t_{a_r}) = \sum_{x \in K_{r}}{\sum_{y \in K_{a}}{\hat{slc}_{deramp}(x,y) * k(x,y)}}.

The computation of the integer component of the coordinates must be intended in this way:

- For each entry :math:`t_{r_s}[i]` of :math:`t_{r_s}`, in general :math:`t_{r_s}[i]` does not belong to the secondary image range grid, and :math:`\hat{t}_{r_s}[i]` is the element in the secondary image range grid that best approximates :math:`t_{r_s}[i]`;
- The same applies in the azimuth direction.

After these considerations, the computation of the fractional component is straightforward and well defined.

By applying this resampling approach, where each output point is independent, the parallelization of the algorithm becomes straightforward.

Detailed variable description
-----------------------------

.. list-table:: Variable Description Table
   :widths: 25 50
   :header-rows: 1

   * - Property
     - Value
   * - Symbol
     - :math:`SLC_{deramp}`
   * - Description
     - Input (real or complex deramped) SLC image
   * - Purpose
     - Input
   * - Units
     - N/A
   * - Type
     - float/complex matrix
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
     - :math:`(t_{r_r}, t_{a_r})`
   * - Description
     - Desired (output) reference range/azimuth grid
   * - Purpose
     - Input
   * - Units
     - (seconds, nanoseconds)
   * - Type
     - (float, datetime64[ns])
   * - Dimensionality
     - (range, azimuth)
   * - Range of values
     - (:math:`\ge 0`, N/A)
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`(\Delta t_{r_s}, \Delta t_{a_s})`
   * - Description
     - Range/azimuth offsets of the secondary image grid, with respect to the reference range/azimuth grid
   * - Purpose
     - Input
   * - Units
     - (seconds, nanoseconds)
   * - Type
     - (float, timedelta64[ns])
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
     - :math:`CSLC_{deramp}`
   * - Description
     - Output (real or complex deramped) coregistered SLC image
   * - Purpose
     - Output
   * - Units
     - N/A
   * - Type
     - float/complex matrix
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
     - :math:`(S_r, S_a)`
   * - Description
     - Interpolation kernel range/azimuth sizes
   * - Purpose
     - Internal
   * - Units
     - N/A
   * - Type
     - (int, int)
   * - Dimensionality
     - N/A
   * - Range of values
     - (:math:`\ge 0`, :math:`\ge 0`)
   * - Initial/default values
     - (11, 11)
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`\beta_{kaiser}`
   * - Description
     - Shape parameter of the Kaiser window
   * - Purpose
     - Input
   * - Units
     - N/A
   * - Type
     - float
   * - Dimensionality
     - N/A
   * - Range of values
     - :math:`\ge 0`
   * - Initial/default values
     - 6
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`(K_r, K_a)`
   * - Description
     - Interpolation kernel samples along range/azimuth, based on the kernel size :math:`(S_r, S_a)`
   * - Purpose
     - Internal
   * - Units
     - N/A
   * - Type
     - (float array, float array)
   * - Dimensionality
     - (range samples, azimuth samples)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`(t_{r_s}, t_{a_s})`
   * - Description
     - Coordinates of the output reference grid in the secondary image grid
   * - Purpose
     - Internal
   * - Units
     - (seconds, nanoseconds)
   * - Type
     - (float, datetime64[ns])
   * - Dimensionality
     - (range, azimuth)
   * - Range of values
     - (:math:`\ge 0`, N/A)
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`(\hat{t}_{r_s}, \hat{t}_{a_s})`
   * - Description
     - Integer part of the output reference grid in the secondary image grid
   * - Purpose
     - Internal
   * - Units
     - (seconds, nanoseconds)
   * - Type
     - (float, datetime64[ns])
   * - Dimensionality
     - (range, azimuth)
   * - Range of values
     - (:math:`\ge 0`, N/A)
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`(\delta t_{r_s}, \delta t_{a_s})`
   * - Description
     - Fractional part of the output reference grid in the secondary image grid
   * - Purpose
     - Internal
   * - Units
     - (seconds, nanoseconds)
   * - Type
     - (float, timedelta64[ns])
   * - Dimensionality
     - (range, azimuth)
   * - Range of values
     - (:math:`\ge 0`, N/A)
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`k`
   * - Description
     - Interpolation kernel, obtained from the matrix multiplication of the two kernel vectors :math:`k_x` and :math:`k_y`
   * - Purpose
     - Internal
   * - Units
     - N/A
   * - Type
     - float matrix
   * - Dimensionality
     - (range samples, azimuth samples)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`\hat{slc}_{deramp}`
   * - Description
     - Input (real or complex deramped) SLC image, windowed according to the interpolation kernel shape
   * - Purpose
     - Internal
   * - Units
     - N/A
   * - Type
     - float/complex matrix
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


