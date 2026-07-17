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

.. _interpolation:

Interpolation
-------------
The *Interpolation* is the process of reconstructing the values in a set of points, starting from the known values in correspondence of another set of points. Depending on the distribution of the input and output points different approaches can be followed.

- :ref:`Regular grid to sparse grid interpolation <regular_grid_to_sparse_grid_image_interpolation_sinc>`: used to resample sencondary image into the same grid of the reference image using windowed sinc() interpolation.
- :ref:`Sparse grid to regular gris interpolation <sparse_grid_to_regular_grid_image_interpolation_linear>`: used to perform linear interpolation of values in correspondence of DEM points to Radar coordinate reference system.
