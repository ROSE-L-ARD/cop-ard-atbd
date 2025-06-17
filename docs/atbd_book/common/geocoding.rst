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

.. _geocoding:

Geocoding
---------------
The *Geocodingt* is the process of mapping data from Radar to ground coordinate reference system. Two possible approaches are considered:

- :ref:`Point projection <phase_geocoding>`: used to map the correspondence between points in ground to Radar coordinates, and interpolate on the transformed points the complex ore real values. This kind of interpolation is uded when the expected resolution of the input and output product are similar (e.g. GSLC).
- :ref:`Point projection <area_projection_geocoding>`: used to map the area covered by a cell in ground coordinates to Radar coordinates and integrate all the involved Radar cells to provide the corresponding value on the ground. This is used in the generation of of all geocoded products where a multilook has to be performed (e.g. NRB, ORB, GCOV, GMLC, GINT, etc.)
