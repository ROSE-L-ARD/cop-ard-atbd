.. _phase_reramping:

Phase reramping
~~~~~~~~~~~~~~~~~~~~~~~~

Overview
--------
The Sentinel-1 TOPS acquisition mode features RAW and SLC data with linear frequency modulation over time.
The reramping procedure restores the original linear frequency modulation after the image resampling step. This procedure modulates the signal to restore the original image spectrum.
Reramping uses the same phase model described in the deramping procedure, except that it must be computed in correspondence with the resampled coordinates.
This document defines the procedure for performing the reramping modulation of Sentinel-1 TOPS IW, EW, and SM Level-1 SLC products.

The following figure presents a schematic overview of this process:

.. figure:: images/Reramping_diagram_v1.drawio.png
   :name: Reramping_diagram_schema
   :align: center
   :width: 600

   Diagram of image reramping processing step. The output is stored in the *EOProductStorage*.

Inputs
------

The *phase reramping* tool requires the following inputs:

- :math:`annot`: L1 Image annotations
- :math:`slc`: Calibrated L1 data

Outputs
-------
The *phase reramping* tool produces complex L1 data with unaltered amplitude and modified phase,
resulting in a modulated signal.

Processing parameters
---------------------
None  

Algorithm
---------
The *phase reramping* process must account for both TOPSAR modulation (for IW and EW acquisition modes)
and the presence of a Doppler centroid.
The mechanism to reconstruct the TOPSAR modulation is extensively explained in {cite}`RDTOPSDEMOD`.  

The Doppler centroid is provided in a Look-Up Table (LUT).  
Starting from this, a polynomial interpolator can be used to reconstruct the phase function over all points of interest :math:`(t_a,t_r )`.  
Notice that in this case, the model must be reconstructed in different coordinates: the azimuth :math:`t_{a_s}` and slant range :math:`t_{r_s}` of the secondary image,
aligned with the output grid (reference image).  

Let :math:`\phi_{demod} (t_{a_s},t_{r_s} )` be the total demodulation phase. The final demodulated SLC :math:`slc' (t_a,t_r )` is:

.. math::
   :label: eq_reramping

   slc' (t_a,t_r ) = slc (t_a,t_r ) e^{j\phi_{demod} (t_{a_s},t_{r_s} ) }

:eq:`eq_reramping`