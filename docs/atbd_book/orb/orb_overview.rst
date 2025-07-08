Overview
========

The CEOS ARD Ocean Radar Backscatter (ORB) product is a full-resolution
intensity product with the necessary corrections applied to allow a
nominal interpretation as a Normalized Radar Cross Section (NRCS,
:math:`\sigma_0`). The CEOS specification of the ORB product, closely
related to the NRB product, includes geoid correction, to convert to
:math:`\sigma_0` but it does not include any despeckling. This choice is
questionable given that the azimuth resolution of a SAR image is limited
not by the radar characteristics or the processed Doppler bandwidth, as
over land, but by the coherence time of the surface as observed by the
radar. This results in the so-called azimuth cut-off,
:raw-latex:`\begin{equation}
        \lambda_c \approx \frac{R\cdot \sigma_v}{v_\mathrm{orb}},
    \end{equation}` with :math:`R` the slant-range to the surface and
:math:`v_\mathrm{orb}` the orbital velocity of the satellite. The result
is that the effective azimuth resolution of the intensity image is
limited to 50 - 400 meters, depending on the sea state, which, in turn,
is mostly wind-driven. Most notably, this effective resolution is
largely wavelength independent, which would, in principle, facilitate
the creation of intercomparable products by different sensors, if these
are first averaged to a generally achievable spatial resolution.

A full resolution product is still useful for the detection of ships or
other anthropogenic targets, for which the :math:`\sigma_0` convention
is not particularly useful. Ship detection could be done starting from
the NRB product. Providing a :math:`\sigma_0` product is a logical
choice when treating the data as an image of a locally homogeneous
distributed surface scatterer. For applications where the NRCS is
relevant (e.g. surface stress or wind, oil-spill detection), a
low-speckle spatially averaged product including polarimetric
information, and a compensation of the known part of the angle of
incidence dependence is preferable to a full-resolution product which
first needs to be properly despeckled, noting that speckle filtering
requires a level of expertise that makes the product deviate from the
ARD rationale.

It also is worth noting that a full-resolution ORB product is, in
general, not a good starting point for the generation of enhanced ocean
products. In many cases, the generation of these products requires SLCs
(or even raw data), for example for sub-look generation to enable the
computation of intensity cross-spectra, or for the optimal suppression
of azimuth ambiguities in coastal areas by optimal selection of the
azimuth-wavenumber (AKA Doppler frequency) weighting.
