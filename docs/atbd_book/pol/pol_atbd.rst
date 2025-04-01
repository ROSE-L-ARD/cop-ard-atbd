
.. _pol_label:

=================================================
Algorithm Theoretical Basis Document (ATBD) - POL
=================================================


Overview
========

The Normalized Radar Backscatter (NRB) product was the first among the Analysis Ready
Data (ARD), with its introduction by CEOS in 2017 and with its definition further refined in 2021
with the release of version 5.5 of the document :cite:`CEOS-ARD_PFS_NRB`. Today, various product specifications
for radar products have been merged into the initial version of the "Combined CEOS-ARD for
Synthetic Aperture Radar" [22]. This product exclusively contains backscatter values and undergoes
Radiometric Terrain Correction (RTC), providing Gamma-Nought as defined in [112],
which mitigates the impact of differing observation geometries. It is the most readily comprehensible
product, enabling direct visualization for visual interpretation, as well as deeper analysis.

Indeed, analysing backscatter time series can yield information regarding the observed object's
type for classification purposes (land use, land cover), as well as its temporal variations,
enabling applications such as change detection, security applications, and vegetation growth
monitoring.

NRB products have gained significant advancements in recent years, driven by both technological
innovation and increasing demand for high-quality, precise data. In the scientific literature,
numerous studies have explored the potential of NRB products for a wide range of applications.
Sentinel-1 satellites, equipped with SAR instruments, provide continuous and systematic observations,
facilitating the generation of NRB products at unprecedented spatial and temporal
resolutions. A pioneering example of NRB product, derived from Sentinel-1 GRD data, is provided
within the "Digital Earth Africa" program [128]. Concurrently, NRB products from other
missions, such as ALOS-2, have also been developed [62].

Looking ahead, upcoming satellite missions acquiring data systematically at L-Band (e.g., NISAR,
ROSE-L) and freely distributing data to the scientific community will enhance observational capabilities
and address various challenges associated with single radar band measurements.


Product Description
======================

The Normalized Radar Backscatter (NRB) product is foreseen and provided in several projects
and it is the main ARD product in the portfolio of different operative and programmed missions.


Main variables
------------------

- **Gamma0** :math:`\gamma_0`: 

- **Local incidence angle** :math:`\theta_i`: 

- **Area Normalization Factor** :math:`ANF`:

- **Number of looks** :math:`N_L`:

- **Mask (Layover/shadow)** :math:`M`:


Metadata
------------

...

Input data
=============

SAR data
------------



Internal data
-----------------



Auxiliary data
------------------

...


Algorithm description
========================


Step1
-----


Step2
-----


Step3
-----



Geocoding
---------
* :ref:`GEOCODING <common_geocoding_label>`


Mosaicking
----------
* :ref:`MOSAIC <common_mosaic_label>`


Data visualization
=====================


Code
=======

.. code-block:: python
    :caption: Import modules

    import rosel.io


Validation and Quality Assessment
=====================================

* Test 1
* Test 2


References
=============

.. bibliography::

Appendices
=============

* [Detailed mathematical derivations]