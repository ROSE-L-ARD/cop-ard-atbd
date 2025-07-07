.. _ggm_product:

=================================
Product Description
=================================

The Geocoded Ground Motion (GGM) product represents the three components of the cumulative displacement vector between
two relatively close dates (tipycally consecutives acquisition dates). 

The GGM product is generated from input data derived using the same methodology (amplitude-based of phase-based GPAO / GPRO products). Therefore,
it is not possible to combine pixel offset products obtained through amplitude cross-correlation
with those derived from phase information, due to the significantly different sensitivity and accuracy
of the input measurements.


Main output variables
---------------------

GGM product consists of the following main variables:

- **displacement_north**: Displacement in the North direction, in meters, geo-projected on the ground reference system.
- **displacement_east**: Displacement in the East direction, in meters, geo-projected on the ground reference system.
- **displacement_vertical**: Displacement in the vertical direction, in meters, geo-projected on the ground reference system.



