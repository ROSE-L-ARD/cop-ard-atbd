.. Copyright 2023 European Union

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

.. _strip_eq_label:

========================================================
Algorithm Theoretical Basis Document (ATBD)
========================================================

The generation of STRIPEQ products involves the same steps of the :ref:`CSLC/GSLC <cslc_label>` products with some particularities and additional post-processing.
In particular, it is requested:

- :ref:`Enhanced Spectral Diverity (ESD) <esd_matching>`: the application of the data-driven approach for co-registration refinement with Enhanced Spectral Diversity (ESD) technique to achieve sub-pixel azimuth alignment of burst-mode SAR acquisitions
- :ref:`Phase deramping <phase_deramping>` (CSLC/GSLC post-processing): remove the common signal modulation, in order to make easier the geocoding or the resampling of the data. If the only application of interest is SAR interferometry this operation is not strictly necessary, because the common modulation cancel out in the interferogram formulation.
- :ref:`Burst merging <burst_merge>` (CSLC/GSLC post-processing): the mosaicking of the bursts complex valued data. The same procedure followed for NRB product can be adopted. It is assumed that phase discontinuities are already solved at level of co-registration.

