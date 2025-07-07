.. _pro_pao_product:

=================================
Product Description
=================================

Precise Range and Azimuth Offset (PRO & PAO respectively) products represents the estimated offset between pair of SAR acquisition in slant range and azimuth directions. 
These offsets can be obtained exploiting the phase or amplitude information.

The product is available in both:

- Radar geometry (burst-wise or swath-merged)
- Ground-projected

The resolution may vary depending on the applied technique and eìstimation direction. In fact, the sensitivity in slant range direction is higher with respect to azimuth and a significant multilook in azimuth has to be applied ion order to make the two inmformation comparable.

PRO / PAO products will be generated on a common reference radar grid shared by both the Sentinel-1 and ROSE-L missions. The output radar grid of these products will likewise be aligned across both missions, ensuring interoperability and joint usability of products generated from data acquired by either satellite.

The offset estimation are derived from pairs of SAR acquisitions. These products are planned to be generated specifically from pairs of consecutive or time-close acquisitions.


Main output variables
---------------------

PRO / PAO product consist of the following main variables:

- :math:`\Delta _{rg}`: Offsets measured along slant range direction (in meters)    
- :math:`\Delta _{az}`: Offsets measured along azimuth direction (in meters)




