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
- Kaiser window parameter  

Algorithm
---------
The slant range :math:`\Delta t_{r_s}` and azimuth :math:`\Delta t_{a_s}` offsets in the secondary image, corresponding to the reference grid, are generally spatially variant, meaning the interpolation kernel varies point by point. The interpolation kernel is based on a windowed :math:`sinc()` interpolator. Ideally, the resampling could be performed independently for each pixel of the output image. It is assumed that the secondary image is already in baseband (i.e., deramping has been applied).  

Let :math:`(S_{r},S_{a})` be the size of the interpolation kernel, with :math:`K_{r}` defined as :math:`\{-S_{r}/2,...,S_{r}/2\}` and :math:`K_{a}` as :math:`\{-S_{a}/2,...,S_{a}/2\}`. The logical steps performed for each output pixel :math:`(t_{r_r},t_{a_r})` are:

1. Identification of the coordinates in the secondary image corresponding to :math:`(rg_r,az_r)`:

.. math::
    :label: coreg_abs_coord

    (t_{r_s},t_{a_s}) = (t_{r_r},t_{a_r})+(\Delta t_{r_s},\Delta t_{a_s})

:eq:`coreg_abs_coord`

2. Computation of the integer and fractional components of the coordinates in the secondary image:

.. math::
    :label: coreg_int_offset

    (\hat{t_r}_s,\hat{t_a}_s) = round((t_{r_s},t_{a_s}))

:eq:`coreg_int_offset`

.. math::
    :label: coreg_frac_offset

    (\delta t_{r_s},\delta t_{a_s}) = (t_{r_s},t_{a_s}) - (\hat{t_r}_s,\hat{t_a}_s)

:eq:`coreg_frac_offset`

3. Computation of the kernel based on the fractional offset:

.. math::
    :label: coreg_kernel_1

    k_x(x) = sinc(x+\delta t_{r_s}) * w_{kaiser}(x+\delta t_{r_s}), \forall x \in K_{r}

.. math::
    :label: coreg_kernel_2

    k_y(y) = sinc(y+\delta t_{a_s}) * w_{kaiser}(y+\delta t_{a_s}), \forall y \in K_{a}

.. math::
    :label: coreg_kernel_3

    k(x,y) = k_x^T(x,y) * k_y(x,y),

:eq:`coreg_kernel_3`

4. Application of the kernel:

.. math::
    :label: coreg_kernel_apply

    CSLC_{deramp}(t_{r_r},t_{a_r}) = \sum_{x \in K_{r}}{\sum_{y \in K_{a}}{\hat{slc}_{deramp}(x,y) * k(x,y)}}.

:eq:`coreg_kernel_apply`

By applying this resampling approach, where each output point is independent, the parallelization of the algorithm becomes straightforward.