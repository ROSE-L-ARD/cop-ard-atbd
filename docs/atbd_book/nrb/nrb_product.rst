.. _nrb_product:

=================================
Product Description
=================================

Normalized Radar Backscatter (NRB) product overview  
'''''''''''''''''''''''''''''''''''''''''''''''''''

NRB is the mosaicked :math:`\gamma^0`, obtained via two possible processing flows:

1. Starting from SLC data with the same Data Take ID, subjected to the co-registration procedure with respect to a reference image (CSLC);
2. Starting from SLC data with the same Data Take ID, without applying the co-registration procedure with respect to a reference image. In the presence of ETAD corrections, a warp of the image is necessary to compensate for timing errors.

In particular, NRB, like the GSLC product, undergoes Radiometric Terrain Correction (RTC) and is provided in the gamma-nought (:math:`\gamma^0`)
backscatter convention, which mitigates variations caused by different observation geometries and is recommended for most land applications.
It also includes information for converting :math:`\gamma^0` to sigma-nought (:math:`\sigma^0`) backscatter.
NRB products are distributed in tiles with characteristics similar to Sentinel-2 products.

Analyzing backscatter time series can yield information regarding the observed object type for classification purposes (land use, land cover), as well as its temporal variations, enabling applications such as change detection, security applications,
and vegetation growth monitoring. NRB products have gained significant advancements in recent years, driven by both technological innovation and increasing demand for high-quality,
precise data. In scientific literature, numerous studies have explored the potential of NRB products for a wide range of applications.
Copernicus SAR missions provide continuous and systematic observations, facilitating the generation of NRB products at unprecedented spatial and temporal resolutions. In the next future with the introduction of addtional frequencies it will be possible to further increase this capability.

Main output variables
---------------------

- :math:`\gamma^0`: Radiometric Terrain Correction Gamma-Nought backscatter linear scaling image.    

- **local incidence angle**: DEM-based local Incidence angle image [deg]. This variable is present only if the NRB is generated from SLCs. If the NRB is derived from CSLCs, this variable will be null, and the reference_inc_angle metadata will be present.

- **area normalization factor**: Optional variable: area normalization factor or local contributing area, used to obtain the gamma0 coefficient. This variable is present only if the NRB is generated from SLCs. If the NRB is derived from CSLC, this variable will be null, and the reference_anf metadata will be present.


