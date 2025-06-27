.. _area_projection_geocoding:

Area Projection Geocoding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Overview
--------

Area Projection Geocoding enables the projection of both real-valued and complex-valued images from radar geometry to ground geometry, using the Area Projection Matrix (APM).

When the input is a flattened CSLC intensity image expressed as :math:`\gamma^0_r`, the result is the geocoded :math:`\gamma^0_g` map corresponding to the output geographic grid, leading to the generation of an NRB product.

This technique can also be applied to interferometric phase data such as INT or CMLC products, yielding as output the GINT product or the corresponding GMLC product in ground geometry.

In the case of polarimetric data, where the input consists of a covariance matrix (COV) with complex-valued off-diagonal elements, Area Projection Geocoding can be used to derive the GCOV product.

Area Projection Geocoding is suitable for both full-resolution inputs, as in the case of NRB, and for multilooked data, as with GINT, GCOV, and GMLC.

In addition, Area Projection Geocoding can be applied to binary masks—such as layover and shadow maps—allowing their projection to the ground geometry using the same matrix-based interpolation scheme. In this case, floating-point outputs are typically thresholded to recover boolean mask values in the geocoded domain.

Inputs
-------

- :math:`w`: Area Projection Matrix (APM)
- :math:`img_r`: Real or complex valued image in radar geometry

Outputs
--------

- :math:`img_g`: Geocoded image

Algorithm
----------

Area Projection Geocoding enables the projection of both real-valued and complex-valued radar images from radar geometry to ground geometry.  
The process relies on the Area Projection Matrix (APM), which defines the linear combination required to compute the geocoded pixel values on the output geographic grid.

For **real-valued** input data, such as the flattened CSLC intensity image expressed as :math:`\gamma^0`, the geocoded map :math:`\gamma^0_g` is computed as follows:

.. math::
   :label: eq_cell_proj_real

   \gamma^0_{g_x} = \frac{\sum_{i \in M_x} w_{i,x} \gamma^0_{r_i}}{\sum_{i \in M_x} w_{i,x}}

Here, :math:`M_x` denotes the set of radar pixels contributing to the ground pixel :math:`x`, and :math:`w_{i,x}` are the corresponding weights.  
This formulation is equivalent to a weighted multilooking operation and produces the NRB product, and the normalization coefficient in :eq:`eq_cell_proj_1` represents the number of looks :math:`nlook_{x}` associated with output resolution cell :math:`x`.

**Layover and shadow masks** are projected using the same matrix, but since masks are expected to be boolean, the floating-point result of the matrix multiplication is thresholded to restore a binary format.

For **complex-valued** input data—such as interferometric phase (INT), multichannel (CMLC), or covariance matrix (COV) products—Area Projection Geocoding applies the same APM to the complex-valued samples:

.. math::
   :label: eq_cell_proj_complex

   cpx_{g_x} = \frac{\sum_{i \in M_x} w_{i,x} cpx_{r_i}}{\sum_{i \in M_x} w_{i,x}}

where :math:`cpx_{r_i}` is the complex value in radar coordinates and :math:`cpx_{g_x}` is the corresponding geocoded complex value.  
This formulation yields the GINT, GMLC, or GCOV product, depending on the input.

It is assumed that the complex data are already in baseband—i.e., any phase modulation from acquisition geometry has been removed (flattened). If this condition is not met, phase flattening must be applied before geocoding.

In both cases, the projection framework is adaptable to multilooked input and output data. If the radar pixels are averaged prior to projection by a factor :math:`(m_r, m_a)` in slant range and azimuth, the inputs and APM must be adjusted accordingly:

.. math::
   :label: eq_multilook_avg

   \bar{\gamma}^{0}_{r_i} = \frac{1}{m_r m_a} \sum_{l \in I_{r_i}} \gamma^0_{r_l}

.. math::
   :label: eq_multilook_weights

   \bar{w}_{l,x} = \sum_{i \in I_{r_l}} w_{i,x}

Additionally, output cells can be grouped and averaged by summing projection weights across neighboring output pixels:

.. math::
   :label: eq_output_averaging

   \hat{w}_{i,l} = \sum_{x \in I_{g_l}} w_{i,x}
