.. _cslc_product:

=================================
Product Description
=================================

Co-registered SLC (CSLC) product overview  
''''''''''''''''''''''''''''''''''''''''''  
Co-registered SLC (CSLC) refers to the output of the SAR co-registration procedure.  
Image co-registration aligns two or more images over a reference radar grid so that each pixel corresponds to the same point target within the scene,  
often with sub-pixel accuracy. This step is essential for creating multidimensional image stacks and enabling advanced data analysis.  

CSLC includes an SLC image or a stack of interferometric images co-registered relative to a reference (virtual or real) orbit.  

The reference radar grid will be "virtual": it is generated using a nominal reference orbit and nominal sensor parameters.  

Optionally, the reference grid could be real: in this case, it corresponds to the radar grid of an SLC image selected as the reference.  

The global, freely accessible Sentinel-1 acquisitions present a significant opportunity to broaden the user base for these advanced applications.  
To fully leverage this potential, it is crucial to address challenges specific to the unique acquisition modes of the Sentinel-1 mission.  
Efforts must also aim to reduce the dependence on acquisition geometry and apply advanced processing techniques to minimize artifacts,  
ensuring the delivery of high-quality, clean products to users.  

Key features of the Co-registered Single Look Complex (CSLC) product include:  

  - Removal of the topographic phase signature using external Digital Elevation Models (DEMs) and precise orbital data.  
  - Application of atmospheric corrections (for troposphere and ionosphere effects) using ETAD data.  
  - Use of ETAD layers to correct timing information.  

The CSLC product must preserve all original information without introducing distortions, as it serves as the foundation for deriving other Analysis Ready Data (ARD) products.  

CSLC products are provided on burst-basis tiles in radar geometry.  

SAR interferometry, particularly multi-interferogram techniques such as Persistent Scatterer Interferometry (PSI),  
Small Baseline Subset (SBAS), or Distributed Scatterers (DS), relies on co-registered images.  
All techniques requiring temporal analysis need co-registered SAR images.  
The availability of CSLC data reduces processing time for analysis chains and overcomes complex co-registration and correction operations, expanding SAR data accessibility to non-expert users.  

Main output variables
---------------------

- **cslc**: Co-registered single look complex stack of data ready for interferometry:

    - the amplitude is in :math:`\β_{LUT}^0` convention, obtained by the calibration step using beta-zero LUT from the SLC annotations; 
    - the phase corresponds to the interpolated and resampled SLC flattened phase with respect to the reference orbit and the input Digital Elevation Model (DEM)
    

- **phase_model**: Topographic phase model, in rad, removed from the original image phase.


.. _gslc_overview:

Geocoded Single Look Complex (GSLC) product overview
'''''''''''''''''''''''''''''''''''''''''''''''''''''

GSLC products contain a geocoded CSLC, resampled to an output geographic grid. They are generated from CSLC and exhibit the following characteristics:

  - The GSLC module can be:

    - :math:`\beta^0`, if no RTC procedure is applied;
    - :math:`\gamma^0`, if an RTC procedure is applied to extract the gamma-nought coefficient.
  - It contains a “flattened” phase data layer: this refers to the interferometric phase relative to a reference orbit and a DEM, with the topographic phase contribution removed.

If the GSLC module follows the :math:`\gamma^0` convention, the NRB of a single burst and the Geocoded Single Look Complex products, as defined by CEOS, are interchangeable.

The sample spacing of the GSLC product in the map coordinate directions is comparable to the full-resolution original SLC product.

GSLC products are provided on burst-basis tiles in projected geometry.

The use of GSLC simplifies the work of users by enabling data visualization directly in a GIS environment and allowing the merging of data from different satellites. Even in cases where GSLC is generated from interferometric acquisitions, this product is less rigorous and does not allow for accurate computation of interferometric products themselves (e.g., coherence, multi-looked wrapped and unwrapped phase).


Main output variables
---------------------

- **gslc** :math:`gstack`: Projected SLC or CSLC, with module equal by default to :math:`\beta^0` or, optionally to :math:`\gamma^0`, coefficient and phase equal to the SLC or CSLC.

- **phase_model** :math:`\phi_{mdl}`: Projected topographic phase model, in rad, removed from the original image phase.

- **local incidence angle** :math:`\theta_i`: DEM-based local Incidence angle image [deg]. This variable is present only if the GSLC is provided in the :math:`\gamma^0` convention and is generated from an SLC. If the GSLC is derived from a CSLC, this variable will be null, and the reference_inc_angle metadata will be present.

- **area normalization factor** :math:`anf`: Optional variable: area normalisation factor or local contributing area, used to obtain the gamma0 coefficient. This variable is present only if the GSLC is provided in the gamma0 convention and is generated from a SLC. If the GSLC is derived from a CSLC, this variable will be null, and the reference_anf metadata will be present.

