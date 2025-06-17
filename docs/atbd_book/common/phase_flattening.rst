.. _phase_flattening:

Phase flattening
~~~~~~~~~~~~~~~~~~~~~~~~

Overview
--------
This procedure eliminates the topographic phase contribution from each SLC image’s phase by using an association matrix computed from the external DEM and orbital data. The operation is performed in the radar coordinate reference system, allowing the generation of an interferometric product by simply multiplying the two images forming the interferometric pair, without requiring additional operations.

The following figure shows a schematic overview of this process:

.. figure:: images/Phase_flattening_diagram_v1.png
   :name: coreg_phase_flattening
   :align: center
   :width: 600

   Diagram of the SLC image phase flattening step.

Inputs
------
The *Phase Flattening* tool requires the following inputs:

    - :math:`CSLC_{deramp}`: Coregistered deramped SLC image  
    - (:math:`t_{r_r}`, :math:`t_{r_s}`): Reference and secondary image slant range distance association matrices  

Outputs
-------
The *Phase Flattening* tool provides the following output:

    - :math:`CSLC_{flatten,deramp}`: SLC data flattened for topographic phase contribution  

Processing parameters
---------------------
None  

Algorithm
---------
The flattened SLC computation follows these steps:

1. Compute the simulated phase :math:`\phi_{topo}` associated with the reference (r) and secondary (s) images:

.. math::
    :label: topo_phase

    \phi_{topo} = \frac{2 \pi f_0}{c} (t_{r_s} - t_{r_r})

:eq:`topo_phase`

2. Apply phase demodulation:

.. math::
    :label: rm_topo_phase

    CSLC_{flatten,deramp} = CSLC_{deramp} * e^{-j\phi_{topo}}

:eq:`rm_topo_phase`