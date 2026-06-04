
.. _CSLC_overview:  

==========================================
CSLC Overview
==========================================

Image co-registration involves aligning two or more images so that each pixel corresponds to the same point in the target scene, potentially achieving sub-pixel accuracy. This step is crucial for generating multidimensional stacks of images and facilitating advanced data analysis.

:term:`SAR` interferometry, especially :term:`SAR` multi-interferogram interferometry (:term:`PSI`/:term:`SBAS`/:term:`DS`) applications, is a primary user of co-registered images. The consistent availability of freely accessible, worldwide acquisitions, such as those from Sentinel-1, as well as the upcoming NISAR and ROSE-L missions, holds significant potential for expanding the user base of this technology.

To achieve this objective, it is vital to address specific challenges related to the unique acquisition modes of individual :term:`SAR` missions. Additionally, efforts should focus on maximizing data independence from acquisition geometry and applying advanced processing techniques to mitigate artifacts and deliver clean products to end-users.

In the case of the ROSE-L mission, one possibility is to provide co-registered products in radar geometry :cite:`RD41`, removing the topographic phase signature. This product is referred to as :term:`CSLC` and is the classical product useful for interferometric analyses, including all corrections for geometry (topographic signature), atmosphere (troposphere and ionosphere), etc. This product is the most rigorous, maintaining all the original information without introducing any distortion, and can be used to derive any other :term:`ARD` product.

To enable working directly in ground-projected geometry, :term:`SLC` images can be automatically referenced to a common grid in map geometry (e.g., UTM, UPS, etc.), removing topographic contributions and potential artifacts due to atmospheric or orbital data inaccuracies. In the :term:`CEOS` :term:`ARD` product specification document, this product is referred to as :term:`GSLC`, and a possible solution is based on :cite:author:`Zebker2017,Zheng2017`. This approach simplifies the work of the end-user by enabling data visualization directly in a :term:`GIS` environment and allowing the merging of data from different satellites, though it is less rigorous and does not allow for accurate computation of interferometric products (e.g., coherence, multilooked wrapped and unwrapped phase).
