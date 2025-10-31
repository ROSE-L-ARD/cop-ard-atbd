.. _noise_removal:

Noise removal
'''''''''''''''''''''''''''''

Overview
--------

The *noise removal* tool is used to modify the amplitude of the complex SLC data in order to compensate for estimated noise power.

Inputs
------

The *noise removal* tool requires the following inputs:

- :math:`annot`: L1 Image annotations
- :math:`slc`: L1 Image data


Outputs
-------

The *noise removal* tool provides in output:

- :math:`slc_{nc}`: complex L1 data with modified amplitude after subtraction of the noise power.

Processing parameters
---------------------

No processing parameters are needed for this operation.

Algorithm
----------

Let  :math:`|slc(t_a,t_r)|` be the amplitude of the original SLC image associated with the azimuth :math:`t_a`  and range :math:`t_r` coordinates.  Let :math:`noise(t_a,t_r)` represent the noise corresponding to the image coordinates of interest.

The noise reconstruction can be achieved using polynomial interpolation of the elements in the LUT associated with the image.

The corrected image is obtained by subtracting the noise power from the original image intensity. From a physical standpoint, negative power cannot exist; if it does occur, the value shall be set to zero.

.. math::
   :label: eq_noise_removal

   amp_{nc} (t_a,t_r )= \begin{cases}
   \sqrt{|slc(t_a,t_r )|^2 - noise(t_a,t_r )}, & \text{if } |slc(t_a,t_r )|^2 - noise(t_a,t_r ) \geq 0 \\
   0, & \text{otherwise}
   \end{cases}

The corrected SLC :math:`slc_{nc} (t_a,t_r )` is obtained as follows:

.. math::
   :label: eq_noise_removal_slc

   slc_{nc} (t_a,t_r )= amp_{nc} (t_a,t_r ) e^{j\angle slc(t_a,t_r )}

where :math:`\angle slc(t_a,t_r )` is the phase of the original SLC image.

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
     - :math:`slc_{nc}`
   * - Description
     - Input SLC image, expressed in Digital Number (DN), with modified amplitude after the subtraction of the noise power
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
     - :math:`noise`
   * - Description
     - Noise power, obtained using polynomial interpolation of the elements in the LUT associated with the input SLC image
   * - Purpose
     - Internal
   * - Units
     - N/A
   * - Type
     - float array
   * - Dimensionality
     - (slant range, azimuth)
   * - Range of values
     - :math:`[0,+\infty)`
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`amp_{nc}`
   * - Description
     - Modified amplitude after the subtraction of the noise power
   * - Purpose
     - Output
   * - Units
     - N/A
   * - Type
     - float array
   * - Dimensionality
     - (slant range, azimuth)
   * - Range of values
     - :math:`[0,+\infty)`
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`|slc|^2`
   * - Description
     - Input SLC image power
   * - Purpose
     - Internal
   * - Units
     - N/A
   * - Type
     - float array
   * - Dimensionality
     - (slant range, azimuth)
   * - Range of values
     - :math:`[0,+\infty)`
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`\angle slc`
   * - Description
     - Input SLC image phase
   * - Purpose
     - Internal
   * - Units
     - radians
   * - Type
     - float array
   * - Dimensionality
     - (range, azimuth)
   * - Range of values
     - :math:`[-\pi, \pi)`
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
     - slant range coordinate
   * - Purpose
     - Internal
   * - Units
     - seconds
   * - Type
     - float
   * - Dimensionality
     - (slant range)
   * - Range of values
     - :math:`[0,+\infty)`
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
