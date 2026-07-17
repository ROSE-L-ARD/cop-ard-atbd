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

.. _Common_tools:

Overview
~~~~~~~~~~~~~~~~

This section describes the algorithms used across different processing units in the ARD generation chain.
It includes the algorithms for the following tools:

- :ref:`Interpolation <interpolation>`:

  - :ref:`Regular grid to sparse grid image interpolation <regular_grid_to_sparse_grid_image_interpolation_sinc>`: Interpolates a regularly gridded image onto a sparse grid using truncated sinc interpolation (e.g., CSLC secondary image warping, GSLC geocoding).
  - :ref:`Sparse grid to regular grid image interpolation <sparse_grid_to_regular_grid_image_interpolation_linear>`: Interpolates a scattered set of values onto a dense grid using linear interpolation (e.g., local incidence angle, LOS).

- :ref:`Reference DEM <reference_DEM>`: 
  
  - :ref:`DEM import <reference_DEM_import>`: extract the DEM as is from external files or Copernicus portal.
  - :ref:`DEM resampling <reference_DEM_resampling>`: resample the DEM according to the desired reference system and resolution.

- :ref:`Reference geometry <reference_geometry>`: 
  
  - :ref:`Coordinate conversion <coordinate_conversion>`: Converts coordinates between different systems, such as geographic grid and radar grid.
  - :ref:`Radar rasterization <radar_rasterization>`: Computes the area projection matrix linking ground and radar coordinates, the area normalization factor (ANF in radar coordinates), and the ground incidence angle.
  - :ref:`Radar mapping <radar_mapping>`: Maps variables from ground to radar coordinates, specifically providing layover and shadow masks.

- :ref:`Flattening <flattening>`: 
  
  - :ref:`Noise removal <noise_removal>`: modifies the amplitude of the complex SLC data in order to compensate for estimated noise power. Used in NRB, POL product generation.
  - :ref:`Gamma flattening <gamma_flattening>`: removal of the expected RCS based on the local terrain contributing area and the SAR geometric distortsion. Used in the NRB, GSLC, POL product generation.
  - :ref:`Phase flattening <phase_flattening>`: removal of the topographic signature derived from the DEM, the orbital parameters and SAR geometric acquisition model. Used in CSLC product generation.