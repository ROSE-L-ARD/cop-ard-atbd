.. _gamma_flattening:

Gamma-flattening
'''''''''''''''''''''

Overview
--------
The objective of the :math:`\gamma`-flattening step is to flatten :math:`CSLC` by applying the Area Normalization Factor (:math:`ANF`).  
Depending on the processing parameters, the output of this step can be either the flattened CSLC intensity product or the flattened CSLC complex product.

Inputs
-------

- :math:`ANF`: Area Normalization Factor  
- :math:`CSLC`: Co-registered Single Look Complex image  

Outputs
--------

- :math:`\gamma^0_r`: Flattened CSLC intensity product  
- :math:`CSLC_{flatten}`: Flattened CSLC complex product  

Algorithm
---------
If only the intensity of the CSLC product is requested, extracting the real and imaginary parts of the  
CSLC data and computing the intensity is required.  

Considering the calibration procedure in :ref:`Amplitude calibration <amplitude_calibration>`, the modulus of CSLC represents  
:math:`\beta^0_{LUT}`, calculated using the LUT table extracted from the SLC annotations. Therefore:

.. math::
   :label: eq_CSLC_module

   \beta_0 = \left| CSLC \right |^2 = \Re{(CSLC)}^2 + \Im{(CSLC)}^2

:eq:`eq_CSLC_module`

The :math:`\gamma`-flattening step computes the :math:`\gamma^0` image in radar geometry.  
This step, considering the preliminary evaluation of :math:`ANF` by :ref:`Radar rasterization <radar_rasterization>`, is straightforward.  
:math:`\gamma^0` is obtained by rescaling :math:`\beta^0` using :math:`ANF`:

.. math::
   :label: eq_gamma_flat

   \gamma^0_r = \beta^0 / ANF

:eq:`eq_gamma_flat`

If the complex flattened CSLC product is requested, :math:`CSLC_{flatten}` is obtained by dividing the CSLC complex product by the square root of :math:`ANF`:

.. math::
   :label: eq_CSLC_flat

   CSLC_{flatten} = CSLC / \sqrt{ANF}

:eq:`eq_CSLC_flat`