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

===========================================
Algorithm Theoretical Basis Document (ATBD) 
===========================================

The generation of interferometric phase and coherence is a relatively straightforward process when starting from CSLC products, which are ready for interferometry.  
In CSLC products, the topographic contribution has been removed, and the model-based and the data-driven approaches compensate for both tropospheric and ionospheric effects.  
Once the interferometric phase and coherence are estimated, the phase can be unwrapped.
Finally the geocoding tools described in :ref:`Geocoding <geocoding>`, can be applied to project the data from radar to ground coordinates.

The processing unit includes the following steps:

- :ref:`interferogram and coherence generation <interf_cohe>`  
- :ref:`phase unwrapping <unwrap>`  


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
   interf_ml = (cstack * cstack.sel(acquisition_date=reference).conj()).coarsen(azimuth_time=L_a, slant_range_time=L_a, boundary='trim').mean()

   # compute the average intensity
   intensity_ml = (np.abs(cstack)**2).coarsen(azimuth_time=L_a, slant_range_time=L_a, boundary='trim').mean()

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

The absolute interferometric phase :math:`\phi ^{unw} _{r,s}` is the unambiguous phase proportional to the differential range between the interferometric pair :math:`(r,s)`.
Starting from the complex interferogram, only the principal values of the phase can be directly measured, i.e. the measured phase values are known only modulo :math:`2 \pi`. The measured **wrapped** phase :math:`\phi _{r,s}` and **unwrapped** phase :math:`\phi ^{unw} _{r,s}` are related by:


.. math::
   :label: phase_unwrapping

   \phi ^{unw} _{r,s} = \phi _{r,s} + 2 \pi n_{r,s}

where :math:`n_{r,s}` is an integer number representing the number of :math:`2 \pi` cycles that must be added to the wrapped phase to obtain the unwrapped phase.
The unwrapping process aims to estimate the integer values of :math:`n_{r,s}` for each point in the interferometric phase image, allowing the reconstruction of the absolute phase.

The phase unwrapping is an ill-posed problem and the determination of the integer values :math:`n_{r,s}` is not unique.
The most common approach in 2D phase unwrapping is to consider phase gradients :math:`\nabla \phi ^{unw} _{r,s}` and find the corrections to the initial estimates (wrapped gradients :math:`\nabla \phi _{r,s}`) in order to meet irrotationality constraints (the value of the phase in correspondence of a points must be independent on the integration path), minimizing a **cost function**. 

Depending on the cost function, different algorithms can be used to solve the phase unwrapping problem. One of the most used open-source algorithm for phase unwrapping processing is based the "Statistical-Cost Network-Flow Algorithm for Phase Unwrapping" :cite:`SNAPHU`. SNAPHU formulates the phase unwrapping problem as a maximum a posteriori (MAP) estimation problem. Its goal is to determine the set of unwrapped phase gradient values :math:`\nabla \phi ^{unw} _{r,s}`  that maximize the posterior distribution :math:`f_{\nabla \phi ^{unw} _{r,s}} \left( \nabla \phi ^{unw} _{r,s} | \nabla \phi _{r,s} \right)`, given the set of wrapped phase gradients :math:`\nabla \phi _{r,s}` .

Different statistical models may be applied for the probability density functions (PDFs) :math:`f_{\nabla \phi ^{unw} _{r,s}}`, depending on the characteristics of the interferometric phase. The cost function can include also information about image intensity and interferometric coherence. The constraints matrix has unimodular structure, and the solution considering linear cost functions with non negative weights, has integer values as expected in phase unwrapping.

In addition in this case the phase unwrapping problem can be transformed in a dual problem of *network flow optimization* :cite:`costantini1998phase`. 

Detailed variables description
''''''''''''''''''''''''''''''

.. list-table:: Variable Description Table
   :widths: 25 50
   :header-rows: 1

   * - Property
     - Value
   * - Symbol
     - :math:`S`
   * - Description
     - Stack of coregistered SLC images
   * - Purpose
     - Input
   * - Units
     - N/A
   * - Type
     - complex float array
   * - Dimensionality
     - (acquisition date, slant range, azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`L_r`
   * - Description
     - Number of looks in slant range direction
   * - Purpose
     - Input
   * - Units
     - N/A
   * - Type
     - int
   * - Dimensionality
     - scalar
   * - Range of values
     - :math:`\mathbb{N}^+`
   * - Initial/default values
     - 1
   * - Name in pseudo-code
     - N/A
   * - 
     - 
   * - Symbol
     - :math:`L_a`
   * - Description
     - Number of looks in azimuth direction
   * - Purpose
     - Input
   * - Units
     - N/A
   * - Type
     - int
   * - Dimensionality
     - scalar
   * - Range of values
     - :math:`\mathbb{N}^+`
   * - Initial/default values
     - 1
   * - Name in pseudo-code
     - N/A
   * - 
     - 
   * - Symbol
     - :math:`\phi_{r,s}`
   * - Description
     - Interferometric phase (considering a reference/secondary images pair)
   * - Purpose
     - Output
   * - Units
     - radians
   * - Type
     - float array
   * - Dimensionality
     - (slant range, azimuth)
   * - Range of values
     - :math:`[-\pi, \pi)`
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`\Gamma_{r,s}`
   * - Description
     - Interferometric coherence (considering a reference/secondary images pair)
   * - Purpose
     - Output
   * - Units
     - N/A
   * - Type
     - float array
   * - Dimensionality
     - (slant range, azimuth)
   * - Range of values
     - :math:`[0,1]`
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`\phi^{unw}_{r,s}`
   * - Description
     - Unwrapped interferometric phase (considering a reference/secondary images pair)
   * - Purpose
     - Output
   * - Units
     - radians
   * - Type
     - float array
   * - Dimensionality
     - (slant range, azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`I_{r,s}`
   * - Description
     - Complex interferogram (considering a reference/secondary images pair)
   * - Purpose
     - Internal
   * - Units
     - N/A
   * - Type
     - complex float array
   * - Dimensionality
     - (slant range, azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A