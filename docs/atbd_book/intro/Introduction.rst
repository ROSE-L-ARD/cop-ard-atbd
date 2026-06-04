.. _Introduction:

Purpose of the document
==============================  

This Jupyter Book documents the Algorithm Theoretical Basis Documents (ATBDs) for the generation of the following Analysis Ready Data (ARD) products: 

* Co-registerd Single Look Complex :ref:`(CSLC/GSLC) <CSLC_overview>`,
* Co-registered multilooked phase :ref:`(CMLP/GMLP) <mlc_overview>`.

A section is dedicated also to the set of common algorithms shared between the different processing chains :ref:`(Common algorithms) <Common_tools>`.

Context
==============================
While traditional SAR products like RAW and SLC are designed for SAR experts and highly specialized users,  
many potential users—such as scientists and application-focused practitioners—could greatly benefit from  
the availability of Analysis Ready Data (ARD) products. These products simplify the use of SAR data,  
allowing users to focus on extracting valuable insights without grappling with the complexities of  
sensor-specific characteristics or advanced calibration procedures.  

By providing pre-processed and standardized data, ARD products make Sentinel-1 data more accessible to a broader audience,  
enabling non-experts to harness the unique capabilities of radar measurements.  
This increased usability could significantly boost the adoption of Sentinel-1 data across diverse application areas,  
such as environmental monitoring, agriculture, and disaster management.  
However, it is essential to ensure that ARD products retain the integrity of the original data,  
avoiding any loss or distortion of the information they carry.  

In general, SAR Analysis Ready Data (ARD) is defined to simplify and standardize the utilization  
of SAR data across a wide range of applications. The Committee on Earth Observation Satellites (CEOS)  
is promoting SAR ARD through a set of data standards and guidelines aimed at  
enhancing the quality, interoperability, and accessibility of EO data acquired from various satellite SAR missions.  

CEOS defines ARD as (see :cite:`CEOS-ARD_PFS_SAR`):  

“CEOS Analysis Ready Data (CEOS-ARD) are satellite data that have been processed to a \
minimum set of requirements and organized into a form that allows immediate analysis with a \  
minimum of additional user effort and interoperability both through time and with other \
datasets.”  


Acknowledgments
===============

We would like to express our sincere gratitude to all the members of the project team and organizations for their invaluable contributions to this work.

Project team members
--------------------

* **Alessio Morea (B-open Solutions)**

* **Federico Minati (B-open Solutions)**

* **Francesco Trillo (B-open Solutions)**

* **Francesco Vecchioli (B-open Solutions)**

* **Carmine Frascella (B-open Solutions)**

* **Alejadro Mestre-Quereda (Universitad de Alicante)**

* **Juan M Lopez-Sanchez (Universitad de Alicante)**

* **Francesco De Zan (Delta-phi)**

* **Paco Lopez-Dekker (TU-Delft)**

* **Yan Yuan (TU-Delft)**

Organizations
-------------

* `ESA <https://www.esa.int>`_: The project has been deveopled under ESA contract 4000144699/24/I-NS.

* `CONAE <https://www.argentina.gob.ar/ciencia/conae>`_ and `ASI <https://www.asi.it/>`_: giving access to SAOCOM datasets.
  
* `JAXA <https://global.jaxa.jp/>`_: giving access to ALOS2 PALSAR datasets.
    

We are also grateful to any individual or group that contributed in other ways, even if they are not directly named here.
