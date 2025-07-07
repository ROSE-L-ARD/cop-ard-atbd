.. _POL_overview:

==========================================
Overview
==========================================

Polarimetric data have been used for many years in a wide range of applications :cite:`Hajnsek2021`,
but until recently there has not been any effort dedicated to defining ARD products or standard formats
for polarimetric data.

The combined CEOS ARD Product Family Specification (PFS) for SAR  :cite:`CEOS_portal` incorporates the
CEOS  PFS for Polarimetric Radar, which defines the Polarimetric Radar (POL) ARD product format as an
extension of the NRB ARD. The POL ARD definition supports Level-1 SLC polarimetric data from any polarimetric
mode, i.e. fully polarimetric, hybrid- or compact-pol, dual-pol, etc. In fact, the single-pol case, i.e.
the mode in which a satellite operates by transmitting one polarisation and receiving one polarisation,
is a subset of the POL ARD which coincides with the NRB ARD.

The POL ARD products considered in this project correspond to the polarimetric covariance matrix
representation, which fully preserves polarimetric content, e.g. the inter-channel polarimetric phases.
The covariance matrix is square with size 3x3 for full-pol (denoted as :math:`C_3`) and with size 2x2 for
compact- and dual-pol modes (denoted as :math:`C_2`).

The product can be provided in radar coordinates (denoted as COV) or in geographical coordinates, i.e. after
geocoding (denoted as GCOV).
