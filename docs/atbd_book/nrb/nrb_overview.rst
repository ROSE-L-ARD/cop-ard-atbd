.. _NRB_overview:

==========================================
Overview
==========================================

Normalized Radar Backscatter (NRB) product overview
''''''''''''''''''''''''''''''''''''''''''''''''''''
NRB is the mosaicked :math:`\gamma^0`, obtained via two possible processing flows:

   1. Starting from SLC S1 data with the same Data Take ID, subjected to the co-registration procedure with respect to a reference image (CSLC);
   2. Starting from SLC S1 data with the same Data Take ID, without applying the co-registration procedure with respect to a reference image. In the presence of ETAD corrections, a warp of the image is necessary to compensate for timing errors.

In particular, NRB, like the GSLC product, undergoes Radiometric Terrain Correction (RTC) and is provided in the gamma-nought (:math:`\gamma^0`)
backscatter convention, which mitigates variations caused by different observation geometries and is recommended for most land applications.
It also includes metadata for converting :math:`\gamma^0` to sigma-nought (:math:`\sigma^0`) backscatter.
NRB products are distributed in tiles with characteristics similar to Sentinel-2 products.

Analyzing backscatter time series can yield information regarding the observed object type for classification purposes
(land use, land cover), as well as its temporal variations, enabling applications such as change detection, security applications,
and vegetation growth monitoring. NRB products have gained significant advancements in recent years, driven by both technological innovation and increasing demand for high-quality,
precise data. In scientific literature, numerous studies have explored the potential of NRB products for a wide range of applications.
Sentinel-1 satellites, equipped with SAR instruments, provide continuous and systematic observations, facilitating the generation of NRB products
at unprecedented spatial and temporal resolutions.