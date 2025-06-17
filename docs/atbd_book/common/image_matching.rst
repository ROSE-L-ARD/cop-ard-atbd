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

