.. _cslc_product:

=================================
Product Description
=================================

Co-registered SLC (CSLC) refers to the output of the SAR co-registration procedure.  
Image co-registration aligns two or more images over a reference radar grid so that each pixel corresponds to the same point target within the scene,  
often with sub-pixel accuracy. This step is essential for creating multidimensional image stacks and enabling advanced data analysis.  

CSLC includes an SLC image or a stack of interferometric images co-registered relative to a reference (virtual or real) orbit.  

The reference radar grid will be "virtual": it is generated using a nominal reference orbit and nominal sensor parameters.  

Optionally, the reference grid could be real: in this case, it corresponds to the radar grid of an SLC image selected as the reference.  

Key features of the Co-registered Single Look Complex (CSLC) product include:

- Removal of the topographic phase signature using external Digital Elevation Models (DEMs) and precise orbital data.  
- Application of timing corrections for troposphere and ionosphere effects, using models (e.g. ETAD) or data driven approaches.

The CSLC product must preserve all original information without introducing distortions, as it serves as the foundation for deriving other Analysis Ready Data (ARD) products.  

CSLC products are provided on burst-basis tiles in radar geometry.  

SAR interferometry, particularly multi-interferogram techniques such as Persistent Scatterer Interferometry (PSI),  
Small Baseline Subset (SBAS), or Distributed Scatterers (DS), relies on co-registered images.  
All techniques requiring temporal analysis need co-registered SAR images.  
The availability of CSLC data reduces processing time for analysis chains and overcomes complex co-registration and correction operations, expanding SAR data accessibility to non-expert users.  

The main output variables are the following:

- **cslc**: Co-registered single look complex stack of data ready for interferometry:
    - the amplitude is in :math:`\beta^0` convention, obtained by the calibration step using beta-zero LUT from the SLC annotations; 
    - the phase corresponds to the interpolated and resampled SLC flattened phase with respect to the reference orbit and the input Digital Elevation Model (DEM)
- **phase_model**: Topographic phase model, in rad, removed from the original image phase.
