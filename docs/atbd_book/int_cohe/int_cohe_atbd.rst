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
.. _int_cohe_label:

========================================================
Algorithm Theoretical Basis Document (ATBD) 
========================================================

The generation of interferometric phase and coherence is a relatively straightforward process when starting from CSLC products, which are ready for interferometry.  
In CSLC products, the topographic contribution has been removed, and the model-based approach compensates for both tropospheric and ionospheric effects.  
Additionally, the estimation of ionospheric effects can be further refined by applying the Split-Spectrum technique.  
Once the interferometric phase and coherence are estimated, the phase can be unwrapped.

The processing unit includes the following steps:

- :ref:`split spectrum <split_spectrum>`  
- :ref:`interferogram and coherence generation <interf_cohe>`  
- :ref:`phase unwrapping <unwrap>`  

.. _split_spectrum:

Split Spectrum
'''''''''''''''''''''''''''''''''''''

Inputs
------

- :math:`S`: stack of co-registered images

Outputs
-------

- :math:`S'`: stack of co-registered images with phase filtered for ionospheric effects

Processing Parameters
---------------------


Algorithm
---------

The Split-Spectrum technique is used to estimate and remove the ionospheric phase contribution from the interferometric phase. The algorithm relies on the assumption that the ionospheric phase contribution is frequency-dependent, whereas the topographic phase contribution is not.

In L-band systems, **one TEC Unit (TECU)**—equivalent to :math:`10^{16}` electrons per :math:`\text{m}^2`—induces approximately **13.6 radians of phase advance**. As a result, any **spatial or temporal variations in TEC** between two SAR acquisitions introduce significant errors in the interferometric phase.

To overcome this limitation, the **Split-Spectrum technique** has emerged as a reliable and robust method for **isolating and estimating the ionospheric phase contribution**, also known as the **ionospheric phase screen**. This technique effectively separates dispersive (ionospheric) and non-dispersive (topographic and tropospheric) phase components in SAR interferograms.

The interferometric phase for a sub-band centered at frequency :math:`f` is given by:

.. math::
   :label: split_spectrum_phase

   \Delta \phi = \frac{4 \pi f}{c} \Delta r_{nd} - \frac{4 \pi K}{c f} \Delta \text{TEC}

where:

- :math:`\Delta \phi` is the interferometric phase at frequency :math:`f`,
- :math:`c` is the speed of light,
- :math:`\Delta r_{nd}` is the non-dispersive change in range between the two acquisitions (residual topography, motion, troposphere),
- :math:`\Delta \text{TEC}` is the differential TEC between the two acquisitions.

This phase corresponds to the sum of the non-dispersive phase :math:`\phi_{nd}` and the dispersive phase :math:`\phi_{iono}`. A linear system of equations can be written for two sub-bands at frequencies :math:`f_0` and :math:`f_1`:

.. math::
   :label: split_spectrum_linear_system

   \begin{bmatrix}
   1 & 1\\
   f_1 / f_0 & f_0 / f_1
   \end{bmatrix}
   \begin{bmatrix}
   \Delta \phi_{nd} \\
   \Delta \phi_{iono}
   \end{bmatrix}
   =
   \begin{bmatrix}
   \Delta \phi_0 \\
   \Delta \phi_1
   \end{bmatrix}

The solution of this system provides estimates of the dispersive (ionospheric) and non-dispersive components of the phase.

Using this simplified notation, the solution for the ionospheric component is:

.. math::
   :label: split_spectrum_solution

   \Delta \phi_{iono} = \frac{f_1}{f_0 + f_1} \left( \Delta \phi_0 - \frac{f_1}{f_0 - f_1} (\Delta \phi_0 - \Delta \phi_1) \right)

In practice, the Split-Spectrum technique computes a weighted difference between the group delay and the phase delay.


.. note::
   - Due to the potentially high rescaling factor in the second term, it is important to filter the differential measurements between the two sub-bands to avoid amplifying noise. This necessitates strong spatial averaging for robust application of the split-spectrum technique, and high frequency ionospheric features may remain uncorrected.

   - The weighted phase combination of :math:`\Delta \phi _0` and :math:`\Delta \phi _1` requires the interferometric phase to be unwrapped when applying the Split-Spectrum technique.

The corrected SLC image :math:`S'` is obtained by applying the ionospheric phase screen to the original SLC images:

.. math::
   :label: split_spectrum_corrected_image

   S' = S \cdot e^{j \Delta \phi _{iono}}


.. _interf_cohe:

Interferogram & coherence generation
'''''''''''''''''''''''''''''''''''''

Inputs
------

- :math:`S`: stack of co-registered images

Outputs
-------

- :math:`\phi_{r,s}`: flattened interferometric phase between the pair :math:`(i, j)` of CSLC images
- :math:`\Gamma_{r,s}`: interferometric coherence between the pair :math:`(i, j)` of CSLC images

Processing Parameters
---------------------

- :math:`L_r, L_a`: number of looks in range and azimuth directions for multilooking (e.g., 5 × 20)

Algorithm
---------

It is assumed that the topographic contribution has already been removed during CSLC generation.  
Therefore, interferogram generation can begin directly with the pixel-wise multiplication of the reference image and the complex conjugate of the secondary image.  

Let :math:`S_r` and :math:`S_s` be the reference and secondary images, respectively.  
Let :math:`I_{r,s}(x, y)` denote the complex interferogram at output point :math:`(x, y)`:

.. math::
   :label: complex_interf

   I_{r,s}(x, y) = \sum_{i = -L_r/2}^{L_r/2} \sum_{j = -L_a/2}^{L_a/2} S_r(x L_r + i, y L_a + j) \cdot S_s^*(x L_r + i, y L_a + j)

The interferometric phase :math:`\phi_{r,s}` is defined as:

.. math::
   :label: phase_interf

   \phi_{r,s} = \angle I_{r,s}

The corresponding interferometric coherence :math:`\Gamma_{r,s}(x,y)` is calculated as:

.. math::

   \Gamma_{r,s}(x, y) = \frac{\left| I_{r,s}(x, y) \right|}
                        {\sqrt{\sum_{i = -L_r/2}^{L_r/2} \sum_{j = -L_a/2}^{L_a/2} \left|S_r(x L_r + i, y L_a + j)\right|^2 \cdot \sum_{i = -L_r/2}^{L_r/2} \sum_{j = -L_a/2}^{L_a/2} \left|S_s(x L_r + i, y L_a + j)\right|^2}}


Notes
-----

- A boxcar was used to perform multilook. In general it would be possible to perform convolution with other user defined filter kernels.
- Coherence provides a quality measure for the interferometric phase.  
- Low coherence regions often correspond to decorrelated areas like vegetation, water bodies, or temporal change.
- In order to obtain more reliable estimation of the coherence, it could be necessary to increase the number of looks, :math:`L_r, L_a`, with respect to the phase estimation 


Code
----------

.. code-block:: python

   import xarray as xr
   import numpy as np

   cstack_file = "/path/to/your/data.zarr"

   # read cslc stack 
   cstack = xr.open_datatree(cstack_file, engine="zarr", chunks={}, decode_coords='all')

   # compute the complex multilooked interferogram
   interf_ml = (cstack * cstack.sel(acquisition_date=reference).conj()).coarsen(azimuth_time=:math:`L_a`, slant_range_time=:math:`L_a`, boundary='trim').mean()

   # compute the average intensity
   intensity_ml = (np.abs(cstack)**2).coarsen(azimuth_time=:math:`L_a`, slant_range_time=:math:`L_a`, boundary='trim').mean()

   # compute coherence
   cohe = interf_ml / np.sqrt(intensity_ml * intensity_ml.sel(acquisition_date=reference))


.. _unwrap:

Phase unwrapping
'''''''''''''''''''''''''''''''''''''

Inputs
------

- :math:`\phi_{r,s}`: interferometric phase
- :math:`\Gamma_{r,s}`: interferometric coherence


Outputs
-------

- :math:`\phi^{unw}_{r,s}`: unwrapped interferometric phase


Algorithm
---------

One of the most used open-source algorithm for phase unwrapping processing is based the "Statistical-Cost Network-Flow Algorithm for Phase Unwrapping" :cite:`SNAPHU`.