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
.. _pro_pao_label:

========================================================
Algorithm Theoretical Basis Document (ATBD)
========================================================

The generation of Precise Range and Azimuth Offsets can follow two different processing workflows depending on the selected measurement strategy:

- phase-based
- amplitude-based

In the phase-based approach, the processing unit includes the following steps:

- :ref:`interferometric processing <int_cohe_label>`: measurement of slant-range offset using the interferometric unwrapped phase and coherence between the reference and secondary images. To distinguish between movement and ionospheric effects, the Split Spectrum technique should be considered in the interferometric flow.
- :ref:`esd <esd_matching>`: measurement of the azimuth offset between the reference and secondary images using the Enhanced Spectral Diversity (ESD) technique, applied to the residual non-dispersive phase component.
- :ref:`forward geocoding <forward_geocoding>`: forward geocoding of the interferometric phase and azimuth offset to obtain range and azimuth offsets in ground geometry.

In the amplitude-based approach, the processing unit includes the following steps:

- :ref:`image matching <image_matching>`: measurement of slant-range and azimuth offsets between the reference and secondary images using the image cross-correlation technique.
- :ref:`forward geocoding <forward_geocoding>`: forward geocoding of the slant-range and azimuth offsets to obtain the corresponding values in ground geometry.

.. note::
   :caption: Note

   The phase-based approach is recommended, as it provides more accurate measurements. However, it requires the availability of two looks to enable continuous azimuth measurements.

   The amplitude-based approach may serve as a fallback solution if two-look ScanSAR acquisitions are unavailable in ROSE-L, or if interferometric coherence is insufficient for phase-based measurement.

   In the phase-based approach, estimation accuracy in the slant-range direction is more than one order of magnitude better than in the azimuth direction. To improve azimuth accuracy—at the expense of resolution—an appropriate multilook filter must be applied (this should be part of more advanced processing, such as GGM).