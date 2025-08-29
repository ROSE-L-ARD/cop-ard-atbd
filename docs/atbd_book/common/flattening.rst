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

.. _flattening:

Flattening
---------------
The *Flatteining* is the process of removing from amplituide or phase signal of the SAR complex image a model:

- :ref:`Noise removal <noise_removal>`: modifies the amplitude of the complex SLC data in order to compensate for estimated noise power. Used in NRB, POL product generation.
- :ref:`Gamma flattening <gamma_flattening>`: removal of the expected RCS based on the local terrain contributing area and the SAR geometric distortsion. Used in the NRB, GSLC, POL product generation.
- :ref:`Phase flattening <phase_flattening>`: removal of the topographic signature derived from the DEM, the orbital parameters and SAR geometric acquisition model. Usded in CSLC product generation.
