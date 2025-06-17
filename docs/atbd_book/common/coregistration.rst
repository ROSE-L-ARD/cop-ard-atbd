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

.. _coregistration:

Co-registration
~~~~~~~~~~~~~~~~~~~~

The *Co-registration Unit* generates Single Look Complex (SLC) images co-registered with respect to a radar reference grid. 
Each pixel of the co-registered SLC (CSLC) images represents the same ground target.

Two different and complementary approaches can be used to align SLC images:

  - :ref:`Model based co-registration <coregistration_model_based>`: Align images with respect to a reference real or virtual image considering DEM, orbital data, timing corrections (e.g. ETAD).
  - :ref:`Data driven co-registration <coregistration_data_driven>`: Align images with respect to a reference real image correcting the deformation between reference and secondary images exploiting image matching techniques.
