.. _mlc_product:

================================
Product Description 
================================

The multi-looked phase consists of one layer for each acquisition date of the input CSLC products. We generate it originally in radar geometry and project it to the ground at the very end. Receiving the product in ground coordinates is important for many users. (Mosaicking should also be considered). The time series of MLC phases can be used to quickly obtain interferometric maps between tow dates or relative deformation time series between two or more points.

Some of the characteristics of this product are shared with the INT and GINT products. All model-driven and data driven corrections (atmosphere, solid earth tides, etc.) can be applied to this product, if they are not already included in the input CSLCs.

The target posting is 50 m, in line with the ROSE-L MRD. Advanced realizations could consider the use of adaptive multi-looking, either with older methods for homogeneous pixel selection or newer machine learning techniques. These are not considered at the moment.

This product includes two quality layers in the form of coherence. Quality layers can be very useful for the user for example to guide space/time phase unwrapping.

The GMLC ground grid is defined to ensure compatibility between missions and products.

Main output variables
---------------------

- **Wrapped multilooked phase** :math:`\phi_n`: This is a temporal collection of phase maps that can be used to generate multi-looked interferograms for any chosen pair of acquisitions in the stack, without having to start from full-resolution images. Taken singularly, each map represents conceptually the interferometric phase between each acquisition and a fixed reference (e.g. the first acquisition in the stack) that one could compute directly by forming an interferogram with the reference. In practice, the direct interferometric phase and the MLC phase will differ: the MLC phase should be less noisy.

- **Long-term coherence** :math:`\gamma^l_n`: This is a temporal collection of coherence maps that represents the long-term coherence of each acquisition with its past. This information can be useful as an indication of the noisiness of interferograms computed between acquisitions that are separated by a large time interval (e.g. 1 year or more). The exact interpretation depends on the chosen processing parameters.

- **Short-term coherence** :math:`\gamma^s_n`: This is a temporal collection of coherence maps that represents the short-term coherence of each acquisition with its recent past. This information can be useful as an indication of the noisiness of interferograms computed between acquisitions that are separated by a short time interval (e.g. a few weeks). The exact interpretation depends on the chosen processing parameters.




Metadata
------------

None (TBC).

