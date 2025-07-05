.. _int_cohe_product:

=================================
Product Description
=================================

INT / COHE / UNW product overview  
''''''''''''''''''''''''''''''''''''''''''  

The Interferogram INT product represents the wrapped phase difference (in radians) between two co-registered SAR acquisitions and is used to analyze surface deformation and coherence. It is generated from CSLC, with corrections applied for co-registration errors (e.g., Enhanced Spectral Diversity) and, when necessary, ionospheric effects (e.g., via split-spectrum technique).

The product is available in both:

- Radar geometry (burst-wise or swath-merged)
- Ground-projected

The resolution may vary depending on the application, from full-resolution (e.g., urban ground deformation) to coarser, multilooked resolutions for regional-scale analyses.

INT / COHE / UNW products will be generated on a common reference radar grid shared by both the Sentinel-1 and ROSE-L missions. The output radar grid of these products will likewise be aligned across both missions, ensuring interoperability and joint usability of products generated from data acquired by either satellite.

The Unwrapped Interferogram UNW product contains the unwrapped phase (in radians), where the :math:`2\pi` ambiguities present in the wrapped interferogram have been resolved. This product enables direct estimation of surface displacement, provided that the phase unwrapping process is successful and robust.

Because phase unwrapping is a known ill-posed problem and no fully reliable algorithm exists that universally guarantees high-quality results, the dissemination of UNW products must be carefully assessed. Their generation is typically limited to areas where sufficient coherence and signal stability allow for accurate unwrapping.

The interferometric products are derived from pairs of SAR acquisitions. These products are planned to be generated specifically from pairs of consecutive or time-close acquisitions.


Main output variables
---------------------

INT / COHE product consist of the following main variables:

- **interferogram**: Wrapped interferometric phase between Secondary and Reference CSLCs, corrected for the topographic contribution and, optionally, for ionospheric and atmospheric effects. Present in INT and UNW and their projected version
    
- **coherence**: The coherence of between the reference and secondary CSLCs forming the interferometric pair polarization

In case un UNW product the following additional layer is present:

- **unwrapped_interferogram**: Unwrapped interferometric phase between the Secondary and Reference CSLCs, corrected for the topographic contribution and, optionally, for ionospheric and atmospheric effects. Present in UNW and its projected version




