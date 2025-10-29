.. _amplitude_calibration:

Amplitude calibration
'''''''''''''''''''''''''''''

Overview
-------- 
An important aspect for the use of slant range complex (SLC) products in the generation of the ARDs is the derivation
of the radar cross-section in case of distributed targets. 

The calibration step derives the radar cross-section (beta naught). These sections of the documents describe how 
the radar cross-section can be calculated specifically for Sentinel-1 products. 
In case of ROSE-L mission the calibration is expected to be performed at SLC product generation level, therefore the SLC products are expected to be already calibrated.


Inputs
------

The *amplitude calibration* tool requires the following inputs:

- :math:`annot`: L1 Image annotations
- :math:`slc`: L1 data


Outputs
-------

The *amplitude calibration* tool provides in output the complex L1 data calibrated in Beta nought :math:`\beta^0`:

- :math:`slc_{ac}`: Calibrated SLC image with amplitude corrected for thermal noise and converted to radar cross-section.

Processing parameters
---------------------

No processing parameters are needed for this operation.

Algorithm
----------

Let :math:`slc (t_a,t_r )` be the image corrected for thermal noise. The amplitude calibration consists of rescaling the amplitude of the complex signal according to a scaling factor :math:`A_c (t_a,t_r )`. This coefficient can be reconstructed using polynomial interpolation of the LUT elements annotated in the input image.

.. math::
   :label: eq_amp_calib

   slc_{ac} (t_a,t_r ) = slc (t_a,t_r ) A_c (t_a,t_r )

Detailed variable description
-----------------------------

.. list-table:: Variable Description Table
   :widths: 25 50
   :header-rows: 1

   * - Property
     - Value
   * - Symbol
     - :math:`slc`
   * - Description
     - Input SLC image, expressed in Digital Number (DN)
   * - Purpose
     - Input
   * - Units
     - N/A
   * - Type
     - complex array
   * - Dimensionality
     - (range, azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`A_c`
   * - Description
     - Amplitude calibration polynomial coefficients' matrix
   * - Purpose
     - Input
   * - Units
     - N/A
   * - Type
     - float matrix
   * - Dimensionality
     - (degree in range, degree in azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`slc_{ac}`
   * - Description
     - Output calibrated SLC in :math:`\beta^0` convention
   * - Purpose
     - Output
   * - Units
     - N/A
   * - Type
     - complex array
   * - Dimensionality
     - (range, azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`t_a`
   * - Description
     - azimuth absolute coordinate
   * - Purpose
     - Internal
   * - Units
     - nanoseconds
   * - Type
     - datetime64[ns]
   * - Dimensionality
     - (azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`t_r`
   * - Description
     - range coordinate
   * - Purpose
     - Internal
   * - Units
     - seconds
   * - Type
     - float
   * - Dimensionality
     - (range)
   * - Range of values
     - :math:`\ge 0`
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
