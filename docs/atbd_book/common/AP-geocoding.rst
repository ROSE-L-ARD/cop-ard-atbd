.. _area_projection_geocoding:

Area Projection Geocoding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Overview
--------

Given the Area Projection Matrix (APM) and the flattened CSLC intensity product in radar geometry, this step allows obtaining the geocoded :math:`\gamma^0` map corresponding to the output geographic grid.

Inputs
-------

- :math:`w`: Area Projection Matrix (APM)
- Layover / shadow mask  
- :math:`\gamma^0_r`: Flattened CSLC intensity product  

Outputs
--------

- :math:`\gamma^0_g`: Geocoded Flattened CSLC intensity product  

Algorithm
----------

AP-Geocoding allows obtaining the :math:`\gamma^0_g` map corresponding to the output geographic grid.  
The Area Projection Matrix defines the linear combination required to compute the correct gamma-nought value for each point of the output geographic grid.

According to the definitions provided in :ref:`Radar rasterization <radar_rasterization>` and :ref:`[RD-SHIROMA-2022] <[RD-SHIROMA-2022]>`, the geocoded :math:`\gamma^0_{g_x}` is obtained by combining :math:`\gamma^0_{r_i}` in radar coordinates with weight :math:`w_{i,x}` for each pixel :math:`i` in the flattened CSLC product in radar geometry, where :math:`x` is the index of the output geographic grid pixel.

Let :math:`M_x` be the set of indices of the flattened CSLC pixels in radar geometry that contribute to the output geographic grid pixel :math:`x`. Geocoding is performed as follows:

.. math::
   :label: eq_cell_proj_1
   
   \gamma^0_{g_x}=\frac{\sum_{i \in M_x} w_{i,x} \gamma^0_{r_i}}{\sum_{i \in M_x} w_{i,x}}

:eq:`eq_cell_proj_1`

The weighted sum in :eq:`eq_cell_proj_1` is equivalent to multilooking, and the normalization coefficient  
represents the number of looks :math:`nlook_{x}` associated with the output resolution cell :math:`x`.

The layover and shadow masks are projected onto the ground using the same procedure. In general, the result of matrix multiplication, as shown in :eq:`eq_cell_proj_1`, produces floating-point values; however, masks are expected to be boolean. A threshold is applied to convert the obtained geocoded values into boolean format.  
