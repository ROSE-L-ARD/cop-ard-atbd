.. _image_matching:

Image matching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Overview
--------

The purpose of this utilitiy is to compute the shift between a reference and a secondary image, by maximizing the module of the Pearson correlation coefficient.
In order to be robust with respect to phase decorrelation effects (long time series or large baselines), it is suggested to consider only the intensity of the image in the computation of the correlation coefficient.

Inputs
-------

- :math:`slc_r`: reference SLC image
- :math:`slc_s`: secondary SLC image

Outputs
--------

- :math:`(\Delta t_{r_s},\Delta t_{a_s})`: offset in slant range and azimuth directios to be applied to the secondary image to match the reference image

Algorithm
----------

The Pearson correlation coefficient between the reference image :math:`slc_r` and the secondary image :math:`slc_s` shifted of :math:`(\Delta t_{r_s},\Delta t_{a_s})` is defined as:

.. math::
    :label: eq_pearson

    \Gamma(\Delta t_{r_s}, \Delta t_{a_s}) = \left | \frac{E\left[ \text{slc}_r(t_{r_s}, t_{a_s}) \text{slc}_s^{*}(t_{r_s}+\Delta t_{r_s}, t_{a_s}+\Delta t_{a_s}) \right ]}{\sqrt{ E \left [ \left| \text{slc}_r(t_{r_s}, t_{a_s}) \right|^2 \right ] E \left [ \left| \text{slc}_s(t_{r_s}+\Delta t_{r_s}, t_{a_s}+\Delta t_{a_s}) \right|^2 \right ]}} \right | 

.. note::
    If the input reference and secondary images are complex-valued, it is important that the phase modulation due to the acquisition mode and acquisition geometry (topography) has been removed.

To find the values :math:`(\Delta t_{r_s}, \Delta t_{a_s})` that maximize the function :math:`\Gamma(\Delta t_{r_s}, \Delta t_{a_s})` with sub-pixel accuracy, it is sufficient to evaluate the function at offsets that are integer multiples of the image spacing. Once the function has been computed at these integer nodes, it is possible to oversample the objective function or fit a paraboloid around the local peak to obtain the coordinates of the maximum.