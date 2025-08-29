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
None 

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
