.. _split_spectrum:

Split Spectrum
'''''''''''''''''''''''''''''''''''''

Inputs
------

- :math:`S`: stack of co-registered images

Outputs
-------

- :math:`S'`: stack of co-registered images with phase filtered for ionospheric effects


Algorithm
---------

The Split-Spectrum technique is used to estimate and remove the ionospheric phase contribution from the interferometric phase. The algorithm relies on the assumption that the ionospheric phase contribution is frequency-dependent, whereas the topographic phase contribution is not.

In L-band systems, **one TEC Unit (TECU)**—equivalent to :math:`10^{16}` electrons per :math:`\text{m}^2`—induces approximately **13.6 radians of phase advance**. As a result, any **spatial or temporal variations in TEC** between two SAR acquisitions introduce significant errors in the interferometric phase.

To overcome this limitation, the **Split-Spectrum technique** has emerged as a reliable and robust method for **isolating and estimating the ionospheric phase contribution**, also known as the **ionospheric phase screen**. This technique effectively separates dispersive (ionospheric) and non-dispersive (topographic and tropospheric) phase components in SAR interferograms.

The interferometric phase for a sub-band centered at frequency :math:`f` is given by:

.. math::
   :label: split_spectrum_phase

   \Delta \phi = \frac{4 \pi f}{c} \Delta r_{nd} - \frac{4 \pi K}{c f} \Delta \text{TEC}

where:

- :math:`\Delta \phi` is the interferometric phase at frequency :math:`f`,
- :math:`c` is the speed of light,
- :math:`\Delta r_{nd}` is the non-dispersive change in range between the two acquisitions (residual topography, motion, troposphere),
- :math:`\Delta \text{TEC}` is the differential TEC between the two acquisitions.

This phase corresponds to the sum of the non-dispersive phase :math:`\phi_{nd}` and the dispersive phase :math:`\phi_{iono}`. A linear system of equations can be written for two sub-bands at frequencies :math:`f_0` and :math:`f_1`:

.. math::
   :label: split_spectrum_linear_system

   \begin{bmatrix}
   1 & 1\\
   f_1 / f_0 & f_0 / f_1
   \end{bmatrix}
   \begin{bmatrix}
   \Delta \phi_{nd} \\
   \Delta \phi_{iono}
   \end{bmatrix}
   =
   \begin{bmatrix}
   \Delta \phi_0 \\
   \Delta \phi_1
   \end{bmatrix}

The solution of this system provides estimates of the dispersive (ionospheric) and non-dispersive components of the phase.

Using this simplified notation, the solution for the ionospheric component is:

.. math::
   :label: split_spectrum_solution

   \Delta \phi_{iono} = \frac{f_1}{f_0 + f_1} \left( \Delta \phi_0 - \frac{f_1}{f_0 - f_1} (\Delta \phi_0 - \Delta \phi_1) \right)

In practice, the Split-Spectrum technique computes a weighted difference between the group delay and the phase delay.


.. note::
   - Due to the potentially high rescaling factor in the second term, it is important to filter the differential measurements between the two sub-bands to avoid amplifying noise. This necessitates strong spatial averaging for robust application of the split-spectrum technique, and high frequency ionospheric features may remain uncorrected.

   - The weighted phase combination of :math:`\Delta \phi _0` and :math:`\Delta \phi _1` requires the interferometric phase to be unwrapped when applying the Split-Spectrum technique.

The corrected SLC image :math:`S'` is obtained by applying the ionospheric phase screen to the original SLC images:

.. math::
   :label: split_spectrum_corrected_image

   S' = S \cdot e^{j \Delta \phi _{iono}}


Detailed variable description
-----------------------------

.. list-table:: Variable Description Table
   :widths: 25 50
   :header-rows: 1

   * - Property
     - Value
   * - Symbol
     - :math:`S`
   * - Description
     - Interferometric stack of co-registered images
   * - Purpose
     - Input
   * - Units
     - N/A
   * - Type
     - complex float array
   * - Dimensionality
     - (slant range, azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`S'`
   * - Description
     - Interferometric stack of co-registered images filtered for ionospheric effects
   * - Purpose
     - Output
   * - Units
     - N/A
   * - Type
     - complex float array
   * - Dimensionality
     - (slant range, azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`\Delta \phi_{iono}`
   * - Description
     - Interferormetic phase component due to ionospheric effects
   * - Internal
     - Output
   * - Units
     - radians
   * - Type
     - float array
   * - Dimensionality
     - (slant range, azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`\Delta \phi_{nd}`
   * - Description
     - Interferormetic phase non dispersive component
   * - Purpose
     - Internal
   * - Units
     - radians
   * - Type
     - float array
   * - Dimensionality
     - (slant range, azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`\Delta \phi_0`
   * - Description
     - Interferormetic phase of the first sub-band
   * - Purpose
     - Internal
   * - Units
     - radians
   * - Type
     - float array
   * - Dimensionality
     - (slant range, azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`\Delta \phi_1`
   * - Description
     - Interferormetic phase of the second sub-band
   * - Purpose
     - Internal
   * - Units
     - radians
   * - Type
     - float array
   * - Dimensionality
     - (slant range, azimuth)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`f_0`
   * - Description
     - Central frequency of the first sub-band
   * - Purpose
     - Internal
   * - Units
     - Hz
   * - Type
     - float
   * - Dimensionality
     - scalar
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`f_1`
   * - Description
     - Central frequency of the second sub-band
   * - Purpose
     - Internal
   * - Units
     - Hz
   * - Type
     - float
   * - Dimensionality
     - scalar
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A