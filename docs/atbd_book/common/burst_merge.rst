.. _burst_merge:

Burst merge
~~~~~~~~~~~~

Overview
---------

The *Burst merge* tool generates homogeneous maps fusing all the layers of the input burst-based NRB products.

Inputs
------
*Burst merge* tool requires the following inputs:

- :math:`\gamma^0_i, \forall i \in \{1,...,N\}`: Burst-projected NRB products, obtained from images with the same Data Take ID  
- :math:`\theta_i, \forall i \in \{1,...,N\}`: Burst-projected local incidence angle, obtained from images with the same Data Take ID  
- :math:`n_i, \forall i \in \{1,...,N\}`: Burst-projected Number of looks associated with each burst-based NRB product  
- :math:`m^l_i, \forall i \in \{1,...,N\}`: Burst-projected Layover masks
- :math:`m^s_i, \forall i \in \{1,...,N\}`: Burst-projected Shadow masks

Outputs
-------
The *Burst merge* tool provides the following output:

- :math:`\gamma^0_{mosaic}`: Geographic tiles of mosaicked NRB map
- :math:`\theta_{mosaic}`: Geographic tiles of mosaicked local incidence angle map
- :math:`n_{mosaic}`: Geographic tiles of mosaicked Number of looks
- :math:`m^l_{mosaic}`: Geographic tiles of mosaicked layover mask
- :math:`m^s_{mosaic}`: Geographic tiles of mosaicked shadow mask
- :math:`id_{mosaic}`: id of the burst used to extract the information 

Algorithms
----------

The modules of the projected NRB product :math:`\gamma^0`, corresponding to each burst, are already calibrated and geocoded using the best available information.  
Points on the output mosaic are selected according to their distance from the center of the burst.  
As the data are calibrated, this enables the generation of seamless mosaicked images.

The reliability associated with each resolution cell of each input map is provided by the number of looks :math:`n`, as computed in :ref:`Area based projection algorithm <radar_rasterization>`.

After aligning all input projected NRB variables listed above, the bursts to be mosaicked are sequentially analyzed following these steps:

- compute the distance from the burst center  
- for points where this distance is smaller than the one already stored:  
   - replace all variables with those of the current burst  
   - update the stored distance for the modified points  
   - save the burst ID for the updated points  

The following figure shows an example of a mosaicked :math:`\gamma^0` map in VH polarization, superimposed onto an optical image from Google Maps.  
The transition between bursts is smooth, and the mosaic appears homogeneous and continuous.

.. _NRB_Mosaicking_nrb_figure:
.. figure:: images/nrb_vh_track_044_s1ard.png
   :name: NRB_Mosaicking_nrb
   :width: 600
   :align: center

   Mosaic of :math:`\gamma^0` in VV polarization, superimposed onto an optical image from Google Maps.

The next figure shows the associated layover/shadow mask. Colors represent:

- cyan: layover  
- orange: shadow  
- red: layover + shadow  

.. _NRB_Mosaicking_mask_figure:
.. figure:: images/mask_track_044_s1ard.png
   :name: NRB_Mosaicking_mask
   :width: 600
   :align: center

   Mosaic of the mask. Cyan corresponds to layover, orange to shadow, and red to both.

The following figure presents a mosaicked local incidence angle map.  
The angle is homogeneous and continuous, as it is not derived from SAR data but simulated using the DEM and orbital information.

.. _NRB_Mosaicking_theta_figure:
.. figure:: images/local_incidence_angle_track_044_s1ard.png
   :name: NRB_Mosaicking_lia
   :width: 600
   :align: center

   Mosaic of the local incidence angle, superimposed onto an optical image from Google Maps.

The new reliability index associated with the mosaic is represented by the number of looks per cell.

The next figure shows a mosaicked nlook map.  
Brighter pixels indicate a higher number of looks, while darker pixels represent lower values.  
This variability mainly reflects terrain slope.

.. _NRB_Mosaicking_nlook_figure:
.. figure:: images/nlook_track_044_s1ard.png
   :name: NRB_Mosaicking_nlook
   :width: 600
   :align: center

   Mosaic of nlooks. Brighter areas correspond to overlapping burst regions with a higher number of averaged pixels.

Each point in the mosaic is tagged with the ID of the source burst from which its data originates.  
A representative map of burst IDs is shown in the following figure.

.. _NRB_Mosaicking_id_figure:
.. figure:: images/id_track_044_s1ard.png
   :name: NRB_Mosaicking_id
   :width: 600
   :align: center

   Mosaic of burst indices, identifying the source burst for each point in the mosaic.


Finally, the mosaicked data are tiled according to the modified Sentinel-2 MGRS grid.

.. note::
   The mosaicking procedure described for real valued data (NRB) can be also applied to complex valued data, such as CSLC in radar geometry, or GSLC in projected geometry.


Detailed variables description
------------------------------

.. list-table:: Variable Description Table
   :widths: 25 50
   :header-rows: 1

   * - Property
     - Value
   * - Symbol
     - :math:`\gamma^0`
   * - Description
     - Input geocoded radar cross-section gamma-naught
   * - Purpose
     - Input
   * - Units
     - N/A
   * - Type
     - float array
   * - Dimensionality
     - (x, y)
   * - Range of values
     - :math:`[0,+\infty)`
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`\theta`
   * - Description
     - Input local incidence angle
   * - Purpose
     - Input
   * - Units
     - radians
   * - Type
     - float array
   * - Dimensionality
     - (x, y)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`n`
   * - Description
     - Input estimated number of looks
   * - Purpose
     - Input
   * - Units
     - N/A
   * - Type
     - float array
   * - Dimensionality
     - (x, y)
   * - Range of values
     - :math:`[0,+\infty)`
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`m^l`
   * - Description
     - Input layover mask
   * - Purpose
     - Input
   * - Units
     - N/A
   * - Type
     - bool array
   * - Dimensionality
     - (x, y)
   * - Range of values
     - :math:`\{0, 1\}`
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`m^s`
   * - Description
     - Input shadow mask
   * - Purpose
     - Input
   * - Units
     - N/A
   * - Type
     - bool array
   * - Dimensionality
     - (x, y)
   * - Range of values
     - :math:`\{0, 1\}`
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`\gamma^0_{mosaic}`
   * - Description
     - Mosaicked Radar cross-section gamma-naught
   * - Purpose
     - Output
   * - Units
     - N/A
   * - Type
     - float array
   * - Dimensionality
     - (x, y)
   * - Range of values
     - N/A
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`\theta_{mosaic}`
   * - Description
     - Mosaicked local incidence angle
   * - Purpose
     - Output
   * - Units
     - radians
   * - Type
     - float array
   * - Dimensionality
     - (x, y)
   * - Range of values
     - :math:`[0,+\infty)`
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`n_{mosaic}`
   * - Description
     - Mosaicked estimated number of looks
   * - Purpose
     - Output
   * - Units
     - N/A
   * - Type
     - float array
   * - Dimensionality
     - (x, y)
   * - Range of values
     - :math:`[0,+\infty)`
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`m^l_{mosaic}`
   * - Description
     - Mosaicked layover mask
   * - Purpose
     - Input
   * - Units
     - N/A
   * - Type
     - bool array
   * - Dimensionality
     - (x, y)
   * - Range of values
     - :math:`\{0, 1\}`
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`m^s_{mosaic}`
   * - Description
     - Mosaicked shadow mask
   * - Purpose
     - Output
   * - Units
     - N/A
   * - Type
     - bool array
   * - Dimensionality
     - (x, y)
   * - Range of values
     - :math:`\{0, 1\}`
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
   * - Symbol
     - :math:`id_{mosaic}`
   * - Description
     - Burst identifier
   * - Purpose
     - Output
   * - Units
     - N/A
   * - Type
     - int array
   * - Dimensionality
     - (x, y)
   * - Range of values
     - :math:`\mathbb{N} \cup \{ -1 \}`
   * - Initial/default values
     - N/A
   * - Name in pseudo-code
     - N/A
   * - 
     -
