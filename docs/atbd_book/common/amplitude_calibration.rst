.. _amplitude_calibration:

Amplitude calibration
'''''''''''''''''''''''''''''

Overview
-------- 
An important aspect for the use of slant range complex (SLC) products in the generation of the ARDs is the derivation
of the radar cross-section in case of distributed targets. 

The calibration step derives the radar cross-section (beta naught). These sections of the documents describe how 
the radar cross-section can be calculated. 


Inputs
------

The *amplitude calibration* tool requires the following inputs:

- :math:`annot`: L1 Image annotations
- :math:`slc_{nc}`: L1 data (corrected for thermal noise)


Outputs
-------

The *amplitude calibration* tool provides in output the complex L1 data calibrated in Beta nought :math:`\beta^0`:

- :math:`slc_{ac}`: Calibrated SLC image with amplitude corrected for thermal noise and converted to radar cross-section.

Processing parameters
---------------------
None


Algorithm
----------

Let :math:`slc_{nc} (t_a,t_r )` be the image corrected for thermal noise. The amplitude calibration consists of rescaling the amplitude of the complex signal according to a scaling factor :math:`A_c (t_a,t_r )`. This coefficient can be reconstructed using polynomial interpolation of the LUT elements annotated in the input image.

.. math::
   :label: eq_amp_calib

   slc_{ac} (t_a,t_r )= slc_{nc} (t_a,t_r ) A_c (t_a,t_r )

:eq:`eq_amp_calib`