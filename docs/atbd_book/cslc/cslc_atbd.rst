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

.. _cslc_label:

========================================================
Algorithm Theoretical Basis Document (ATBD) 
========================================================

The generation of CSLC products involves several complex processing units and an overview of the processing workflow is reported in :numref:`CSLC_diagram`.

.. _CSLC_diagram_figure:
.. figure:: images/CSLC_diagram.drawio.png
   :name: CSLC_diagram
   :width: 600
   :align: center

   *CSLC* generation flow diagram.

In case of GSLC product and additional *Geocoding* functionality is requested and the corresponding workflow is reported in :numref:`GSLC_diagram`.

.. _GSLC_diagram_figure:
.. figure:: images/GSLC_diagram.drawio.png
   :name: GSLC_diagram
   :width: 600
   :align: center

   *GSLC* generation flow diagram.

The processing units involved are:

- :ref:`Calibration <calibration>`: The *Calibration Unit* includes the steps for importing input SLC data, applying noise removal, amplitude calibration, and phase deramping.
- :ref:`Reference DEM <reference_DEM>`: The *Reference DEM Unit* includes the step for generating a DEM interpolated onto the output geographic grid of the geocoded ARD products.
- :ref:`Reference Geometry <reference_geometry>`: The *Reference Geometry Unit* includes all steps required to generate geometric information, stored in intermediate products, and needed by some *Co-registration* and *Geocoding* steps. The outputs of the *Reference Geometry Unit* can be stored in a static archive and reused by other processing units as needed.
- :ref:`Co-registration <coregistration>`: The *Co-registration Unit* produces CSLC products with respect to a reference radar grid. It is possible to apply models (e.g. ETAD corrections), or compute the corrections to the model based coregistration, by applying image cross-correlation with respect to a real reference image.
- :ref:`Geocoding <geocoding>`: The *Geocoding Unit* uses CSLC and geometric information to extract GSLC/NRB products per burst or per swath (in the case of SM products).
