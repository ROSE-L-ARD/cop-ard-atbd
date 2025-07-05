
.. _int_cohe_overview:  

==========================================
Overview
==========================================

Wrapped phase (INT), coherence map (COHE), and unwrapped phase (UNW) are well-established products that are effectively used in a wide range of applications, from infrastructure monitoring in urban areas to ice and glacier observation. These ARDs can be generated at full resolution for applications that require high spatial detail (e.g., ground deformation monitoring), or at coarser, multilooked resolution for studies analyzing deformation signals over broader spatial scales.
A key aspect in creating an interferometric data stack—especially when using multilooked data—is the selection of image pairs. To maximize coherence, consecutive acquisitions are typically chosen for ARD product generation.
Starting from the advanced CSLC product, the workflow for interferometric product generation becomes straightforward. Co-registration refinement is no longer needed, and phase noise can be reduced through optional filtering. The only critical processing step required, in particular for L-band data, is the application of the Split Spectrum technique to further refine the removal of ionospheric artifacts.
Phase unwrapping is a crucial step in the generation of the UNW product, as it resolves the :math:`2\pi` ambiguities present in the wrapped phase. However, it is important to note that phase unwrapping is an ill-posed problem, and no algorithm guarantees perfect results in all scenarios. Therefore, the generation of UNW products should be carefully evaluated based on the coherence and stability of the signal in the area of interest.
