.. _pol_product:

=================================
Product Description
=================================

Polarimetric (POL) product overview
'''''''''''''''''''''''''''''''''''''''''''''''''''

POL is the polarimetric ARD product which corresponds to the polarimetric covariance matrix,
which can be provided in radar coordinates (COV) or in geographical coordinates (GCOV), i.e. after geocoding.

The inputs required to generate these products correspond to individual SLC images or to previously generated
CSLC products. In both cases, the processing required to compute each entry of the covariance matrix is totally
equivalent to what is done to produce NRB products.


The formation of the POL products from the input SLC images consists of three or four steps:
1. Terrain flattening correction (also known as RTC), which can be directly applied to the images in SLC format.
2. Generation of the complex cross-products between polarimetric channels (off-diagonal elements of the covariance matrix), and the real intensity values of each channel (diagonal elements of the covariance matrix).
3. Spatial filtering or multi-looking of every matrix entry.
4. Geocoding of all matrix entries, which is required to produce a GCOV.

The two last steps can be carried out simultaneously, following the approach proposed for NISAR GCOV data. In that case, the extent of the spatial filter depends on the relationship between the size of the output product (posting) and the corresponding pixels in the SLC image, which differs over the image due to topographic slopes.

If a COV product is to be produced, i.e. without geocoding, the spatial filtering step is mandatory to estimate a true covariance matrix.

SAR polarimetry entails the acquisition of images using different combinations of transmitted and received polarisation.
Polarimetric data have been used for many years in a wide range of applications, including forestry, cryosphere, land cover classification, agriculture monitoring, urban studies, oil spill characterization, etc.
The contribution of polarimetry comes from its sensitivity to the geometry and dielectric properties of the scene, which influence the polarisation of the waves received at the radar due to both propagation (e.g. through a vegetation canopy) and scattering (e.g. surface vs dihedral).

Main output variables
---------------------

- **C(i,j)**: Entries of the polarimetric covariance matrix:

    - Diagonal entries :math:`(i=j)` correspond to the backscattering coefficients of the polarimetric channels measured (e.g. VV, VH, etc.), so they are images with positive real numbers.
    - Off-diagonal :math:`(i \neq j)` entries correspond to the complex cross-correlation between different polarimetric channels measured (e.g. VV·VH^*), so they are images with complex numbers. Provided that the covariance matrices are Hermitian, only the off-diagonal elements of the upper-triangular matrix are saved as product layers.




