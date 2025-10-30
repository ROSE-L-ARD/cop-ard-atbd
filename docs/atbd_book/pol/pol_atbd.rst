.. _pol_label:

===========================================
Algorithm Theoretical Basis Document (ATBD)
===========================================

The generation of POL products involves the same processing steps of the NRB products, but
they are applied to additional layers of output data.

Input data
==========

SAR data
--------

The input for the generation of this product is a SLC or a CSLC product, i.e. a stack of
co-registered slc's in radar geometry. In both cases, two or four polarimetric channel
are available is available, depending on whether the images are acquired in dual-pol or
quad-pol mode.

An example with SAOCOM dual-pol data (VV-VH) is used for illustration purposes.

Auxiliary data
--------------

As in the case of NRB, auxiliary information is required for applying the radiometric terrain
correction (RTC) and the geocoding.


Algorithm steps
===============

Read channels and auxiliary layers
----------------------------------

.. code::

        # Read channels as SLC images for a given acquisition date

        slc_vv = rosel.io.read( cslc_path_vv ).cstack.sel( acquisition_date=acquisition_date )
        slc_vh = rosel.io.read( cslc_path_vh ).cstack.sel( acquisition_date=acquisition_date )
        
        # Read auxiliary layers for flattening and geocoding
        
        selection = rosel.io.read( selection_path )
        A = rosel.io.read( rtc_ap_path, mask_and_scale = False ).v

Radiometric terrain correction (RTC)
------------------------------------

.. code:: 

        # Flatten the SLC values of both channels
        
        slc_vv_flat = rosel.shiroma.flatten_radar_image(slc_vv, A, data_path = f"{out_path}/flattened_slc_vv", read=True)
        
        slc_vh_flat = rosel.shiroma.flatten_radar_image(slc_vh, A, data_path = f"{out_path}/flattened_slc_vh", read=True)

Covariance matrix formation: cross-products and estimation
----------------------------------------------------------

The expression of the dual-pol covariance matrix is:

.. math::

    C_2 =
        \begin{bmatrix}
            \langle |VV|^2 \rangle & \langle VV \cdot VH^* \rangle \\
            \langle VH \cdot VV^* \rangle & \langle |VH|^2 \rangle
        \end{bmatrix}

where :math:`\langle \rangle` denotes a spatial averaging or filtering, and superscript :math:`*` is the complex conjugate.

.. code:: 


        if estimation_type == 'MULTI-LOOK': 

            multilook = {"azimuth_time": kernel_size[0], "slant_range_time": kernel_size[1]}
        
            C11 = (np.abs((slc_vv_flat * slc_vv_flat.conj())).astype(np.float32).coarsen(azimuth_time=multilook["azimuth_time"], slant_range_time=multilook["slant_range_time"], boundary="pad")
                .mean().chunk(azimuth_time=300, slant_range_time=300))
            
            C22 = (np.abs((slc_vh_flat * slc_vh_flat.conj())).astype(np.float32).coarsen(azimuth_time=multilook["azimuth_time"], slant_range_time=multilook["slant_range_time"], boundary="pad")
                .mean().chunk(azimuth_time=300, slant_range_time=300))
            
            C12 = (slc_vv_flat * slc_vh_flat.conj()).coarsen(azimuth_time=multilook["azimuth_time"], slant_range_time=multilook["slant_range_time"], boundary="pad").mean().chunk(azimuth_time=300, slant_range_time=300)
        
        elif estimation_type == 'BOXCAR':

            boxcar_kernel = {"azimuth_time": kernel_size[0], "slant_range_time": kernel_size[1]}
    
            data = np.abs((slc_vv_flat * slc_vv_flat.conj())).astype(np.float32)
            C11  = data.rolling( azimuth_time=boxcar_kernel["azimuth_time"], slant_range_time=boxcar_kernel["slant_range_time"], center=True).mean().chunk({"azimuth_time": 1024, "slant_range_time": 1024})
    
            data = np.abs((slc_vh_flat * slc_vh_flat.conj())).astype(np.float32)
            C22 = data.rolling( azimuth_time=boxcar_kernel["azimuth_time"], slant_range_time=boxcar_kernel["slant_range_time"], center=True).mean().chunk({"azimuth_time": 1024, "slant_range_time": 1024})   
                   
            data = slc_vv_flat * slc_vh_flat.conj()
            C12 = data.rolling( azimuth_time=boxcar_kernel["azimuth_time"], slant_range_time=boxcar_kernel["slant_range_time"], center=True).mean().chunk({"azimuth_time": 1024, "slant_range_time": 1024})         
            
        elif estimation_type == 'SHIROMA':

            C11 = np.abs((slc_vv_flat * slc_vv_flat.conj())).astype(np.float32)
    
            C22 = np.abs((slc_vh_flat * slc_vh_flat.conj())).astype(np.float32)
                   
            C12 = slc_vv_flat * slc_vh_flat.conj()
            

Save the COV product
--------------------

.. code:: 

        rosel.io.write(C11.to_dataset(name="v"), f"{out_path}/COV/C11")
        rosel.io.write(C22.to_dataset(name="v"), f"{out_path}/COV/C22")
        rosel.io.write(C12.to_dataset(name="v"), f"{out_path}/COV/C12")



Geocoding and save the GCOV product
-----------------------------------

Geocoding is carried out using Shiroma's approach.
In case of 'MULTI-LOOK' estimation, the output grid can be coarsened.
Otherwise, the output grid posting is similar to SLC resolution.
        
.. code::

        if estimation_type == 'MULTI-LOOK': 
        
            gC11 = rosel.shiroma.map_geo_ap(
                c_path=f"{out_path}/COV/C11",
                simulation=selection,
                data_path_shiroma=shiroma_path,
                data_path_geo_ap=f"{out_path}/GCOV/C11",
                multilook=multilook,
                read=True,
                enable_dask=True,
            )
                
            gC22 = rosel.shiroma.map_geo_ap(
                c_path=f"{out_path}/COV/C22",
                simulation=selection,
                data_path_shiroma=shiroma_path,
                data_path_geo_ap=f"{out_path}/GCOV/C22",
                multilook=multilook,
                read=True,
                enable_dask=True,
            )
                
            gC12 = rosel.shiroma.map_geo_ap(
                c_path=f"{out_path}/COV/C12",
                simulation=selection,
                data_path_shiroma=shiroma_path,
                data_path_geo_ap=f"{out_path}/GCOV/C12",
                multilook=multilook,
                read=True,
                enable_dask=True,
            )
        
        else:
            
            gC11 = rosel.shiroma.map_geo_ap(
                c_path=f"{out_path}/COV/C11",
                simulation=selection,
                data_path_shiroma=shiroma_path,
                data_path_geo_ap=f"{out_path}/GCOV/C11",
                read=True,
                enable_dask=True,
            )
    
            gC22 = rosel.shiroma.map_geo_ap(
                c_path=f"{out_path}/COV/C22",
                simulation=selection,
                data_path_shiroma=shiroma_path,
                data_path_geo_ap=f"{out_path}/GCOV/C22",
                read=True,
                enable_dask=True,
            )
    
            gC12 = rosel.shiroma.map_geo_ap(
                c_path=f"{out_path}/COV/C12",
                simulation=selection,
                data_path_shiroma=shiroma_path,
                data_path_geo_ap=f"{out_path}/GCOV/C12",
                read=True,
                enable_dask=True,
            )
    