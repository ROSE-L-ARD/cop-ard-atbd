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

- :ref:`Calibration`:
  
  - :ref:`Amplitude calibration <amplitude_calibration>`: derive the radar cross-section beta naught or sigma naught according to the input metadata.
  - :ref:`Phase deramping <phase_deramping>`: remove the linear frequency modulation (also called deramping), which is necessary for performing basic operations like interpolation/resampling of the data, often used in interferometric processing chains. In addition, the deramping procedure demodulates the signal to report its spectrum in baseband.
  - :ref:`Phase reramping <phase_reramping>`: restore the original linear frequency modulation after the image resampling step. This procedure modulates the signal to restore the original image spectrum.

- :ref:`Geocoding <geocoding>`:

  - :ref:`Point projection <phase_geocoding>`: used to map the correspondence between points in ground to Radar coordinates, and interpolate on the transformed points the complex ore real values. This kind of interpolation is uded when the expected resolution of the input and output product are similar (e.g. GSLC).
  - :ref:`Area projection <area_projection_geocoding>`: used to map the area covered by a cell in ground coordinates to Radar coordinates and integrate all the involved Radar cells to provide the corresponding value on the ground. This is used in the generation of of all geocoded products where a multilook has to be performed (e.g. NRB, ORB, GCOV, GMLC, GINT, etc.)

- :ref:`Interpolation <interpolation>`:

  - :ref:`Regular grid to sparse grid image interpolation <regular_grid_to_sparse_grid_image_interpolation_sinc>`: Interpolates a regularly gridded image onto a sparse grid using truncated sinc interpolation (e.g., CSLC secondary image warping, GSLC geocoding).
  - :ref:`Sparse grid to regular grid image interpolation <sparse_grid_to_regular_grid_image_interpolation_linear>`: Interpolates a scattered set of values onto a dense grid using linear interpolation (e.g., local incidence angle, LOS).

- :ref:`Flattening <flattening>`:

  - :ref:`Noise removal <noise_removal>`: Modifies the amplitude of the complex SLC data in order to compensate for estimated noise power.
  - :ref:`Gamma flattening <gamma_flattening>`: Modifies the amplitute of complex SLC data to apply terrain slope correction.
  - :ref:`Phase flattening <phase_flattening>`: Modifies the phase of complex SLC data to remove the topographic phase signature.

- :ref:`Reference DEM <reference_DEM>`: 
  
  - :ref:`DEM import <reference_DEM_import>`: extract the DEM as is from external files or Copernicus portal.
  - :ref:`DEM resampling <reference_DEM_resampling>`: resample the DEM according to the desired reference system and resolution.

- :ref:`Reference geometry <reference_geometry>`: 
  
  - :ref:`Coordinate conversion <coordinate_conversion>`: Converts coordinates between different systems, such as geographic grid and radar grid.
  - :ref:`Radar rasterization <radar_rasterization>`: Computes the area projection matrix linking ground and radar coordinates, the area normalization factor (ANF in radar coordinates), and the ground incidence angle.
  - :ref:`Radar mapping <radar_mapping>`: Maps variables from ground to radar coordinates, specifically providing layover and shadow masks.

- :ref:`Co-registration <coregistration>`:

  - :ref:`Model based co-registration <coregistration_model_based>`: Align images with respect to a reference real or virtual image considering DEM, orbital data, timing corrections (e.g. ETAD).
  - :ref:`Data driven co-registration <coregistration_data_driven>`: Align images with respect to a reference real image correcting the deformation between reference and secondary images exploiting image matching techniques.
  
- :ref:`Mosaicking <mosaicking>`: Merge data from multiple bursts belonging to the same datatake ID.
