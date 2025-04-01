
.. _commonalgo_label:

================================================================
Algorithm Theoretical Basis Document (ATBD) - Common Algorithms
================================================================

# Common Algorithms

This section describes algorithms that are common to the generation of multiple ARD products.

.. _common_geocoding_label:

## Geocoding

Geocoding is a process that projects raster data onto a specific map projection. It is essential for ensuring that all ARD products are spatially aligned.

.. code-block:: python
    :caption: Pseudo-code for Geocoding

    def geocode(input_raster, sensor_geometry, output_projection):
        # Apply geocoding algorithm
        geocoded_raster = apply_geocoding(input_raster, sensor_geometry, output_projection)

        return geocoded_raster

.. _common_mosaic_label:

## Mosaic

## Interpolation

Interpolation is used to resample raster data to a different spatial resolution. This is often necessary when integrating data from different sources with varying resolutions.

.. code-block:: python
    :caption: Pseudo-code for Interpolation

    def interpolate(input_raster, output_resolution, method):
        # Apply interpolation algorithm
        interpolated_raster = apply_interpolation(input_raster, output_resolution, method)

        return interpolated_raster

## Coordinate Conversion

Coordinate conversion is used to transform coordinates between different coordinate systems.

.. code-block:: python
    :caption: Pseudo-code for Coordinate Conversion

    def convert_coordinates(input_coordinates, input_crs, output_crs):
        # Apply coordinate conversion algorithm
        output_coordinates = apply_coordinate_conversion(input_coordinates, input_crs, output_crs)

        return output_coordinates

## Cross References

These common algorithms are used in the generation of the following ARD products:

* :ref:`NRB <nrb_label>`
* :ref:`CSLC <cslc_label>`
* :ref:`POL <pol_label>`

