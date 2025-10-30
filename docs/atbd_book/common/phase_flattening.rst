.. _phase_flattening:

Phase flattening
~~~~~~~~~~~~~~~~~~~~~~~~

Overview
--------
This procedure eliminates the topographic phase contribution from each SLC image's phase by using an association matrix computed from the external DEM and orbital data. The operation is performed in the radar coordinate reference system, allowing the generation of an interferometric product by simply multiplying the two images forming the interferometric pair, without requiring additional operations.

Inputs
------
The *Phase Flattening* tool requires the following inputs:

    - :math:`CSLC_{deramp}`: Coregistered deramped SLC image  
    - :math:`\Delta t_{r_s}`: Range offset of the input (secondary) image grid, with respect to the reference range/azimuth grid

Outputs
-------
The *Phase Flattening* tool provides the following output:

    - :math:`CSLC_{flatten,deramp}`: SLC data flattened for topographic phase contribution  

Processing parameters
---------------------
No processing parameters are needed for this operation.  

Algorithm
---------
The flattened SLC computation follows these steps:

1. Compute the simulated phase :math:`\phi_{topo}` associated with the reference and secondary images (:math:`c` indicates the speed of light):

.. math::
    :label: topo_phase

    \phi_{topo} = \frac{2 \pi f_0}{c} \Delta t_{r_s}

2. Apply phase demodulation:

.. math::
    :label: rm_topo_phase

    CSLC_{flatten,deramp} = CSLC_{deramp} * e^{-j\phi_{topo}}

Detailed variable description
-----------------------------

.. list-table:: Variable Description Table
   :widths: 25 50
   :header-rows: 1

   * - Property
     - Value
   * - Symbol
     - :math:`CSLC_{deramp}`
   * - Description
     - Coregistered deramped SLC image  
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
     - :math:`\Delta t_{r_s}`
   * - Description
     - Range offset of the secondary image grid, with respect to the reference range/azimuth grid
   * - Purpose
     - Input
   * - Units
     - seconds
   * - Type
     - float
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
     - :math:`CSLC_{flatten,deramp}`
   * - Description
     - Coregistered deramped SLC image, flattened for topographic phase contribution
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
     - :math:`f_0`
   * - Description
     - Carrier (center) frequency of the transmitted radar signal
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
     - :math:`\phi_{topo}`
   * - Description
     - Computed simulated phase
   * - Purpose
     - Internal
   * - Units
     - radians
   * - Type
     - float
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