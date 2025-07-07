.. _strip_eq_product:

=================================
Product Description
=================================


Main output variables
---------------------

STRIPEQ product consists of the following main variables:

- **cslc**: Debursted and mosaiked co-registered single look complex stack of data ready for interferometry:

    - the amplitude is in :math:`\beta^0` convention, obtained by the calibration step using beta-zero LUT from the SLC annotations; 
    - the phase corresponds to the interpolated and resampled SLC flattened phase with respect to the reference orbit and the input Digital Elevation Model (DEM)
    
- **phase_model**: Topographic phase model, in rad, removed from the original image phase.



