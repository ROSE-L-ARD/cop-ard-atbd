Product Description
===================

Ocean Radar Backscatter (ORB) product overview
----------------------------------------------

The ORB product, either as defined in
:raw-latex:`\cite{CEOS-ARD_PFS_ORB}` or in the variants outlined in the
proposal for this study, can be relatively straightforwardly derived
from the NRB. This derivation provides both the necessary full
resolution and spatially averaged Sigma-Nought (:math:`\sigma_0`) values
on a map-projected grid.

ORB comprises multiple layers of :math:`\sigma_0`, each corresponds to a
specific layer of preprocessing. These preprocessing steps include
denoise, outlier removal, downsampling and surface roughness
normalisation. The intermediate products are also saved, including a
full resolution bright target mask, the noise-equivalent sigma zero
(NESZ), the outlier removed :math:`\sigma_0`, and the angle of incidence
compensated :math:`\sigma_0`. Comprehensive annotations detailing the
processing steps applied to each layer ensures full traceability and
allows users to reverse or reproduce the processing chain as needed.

Main output variables
---------------------

:math:`\boldsymbol{\sigma_{0,\mathrm{raw}}}`: Full resolution outlier
masked :math:`\sigma_0`

:math:`\boldsymbol{\sigma_{0,\mathrm{nesz}}}`: Spatially-averaged, LxL
m2 resolution noise equivalent :math:`\sigma_0`

:math:`\boldsymbol{\sigma_{0,\mathrm{denoised}}}`: Spatially-averaged,
LxL m2 resolution denoised :math:`\sigma_0`

:math:`\boldsymbol{\sigma_{0,\mathrm{L}}}`: Spatially-averaged, LxL m2
resolution denoised and outlier removed :math:`\sigma_0`

:math:`\boldsymbol{\sigma_{0,\mathrm{L}}/\sigma_{0,\mathrm{mod}}}`:
Spatially-averaged, LxL m2 resolution (mean) wind normalized backscatter
:math:`\sigma_0`

