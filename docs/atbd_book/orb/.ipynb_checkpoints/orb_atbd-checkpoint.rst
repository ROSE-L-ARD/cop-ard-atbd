Algorithm Theoretical Basis Document (ATBD)
===========================================

The generation of ORB products involves the same processing steps of the
NRB products, but they are applied to additional layers of output data.

There are five additional steps in processing: data preparation, bright
target removal, downsample, angle of incidence compensation and data
saving.

Most of the processing steps are done with the software developed for
Harmony Analysis Ready Data (HARD)

Data preparation
----------------

The data preparation include three steps. First, load in data. Second,
reproject datatree into longitude and latitude coordinate, which is
essential for searching for the wind products. Third, load in geometry
information which is later used for angle of incidence compensation.

.. code:: ipython3

    import os
    import numpy as np
    import xarray as xr
    import matplotlib.pyplot as plt
    from datatree import open_datatree

.. code:: ipython3

    def reproj_lonlat(ds_sc):
        # Brest falls within UTM Zone 30N
        ds_sc = ds_sc.rio.write_crs("EPSG:32630")
        ds_sc_lonlat = ds_sc.rio.reproject("EPSG:4326")
        sc_lon, sc_lat = np.meshgrid(ds_sc_lonlat.x, ds_sc_lonlat.y)
        ds_sc_lonlat['latitude'] = (['y', 'x'], sc_lat)
        ds_sc_lonlat['longitude'] = (['y', 'x'], sc_lon)
        return ds_sc_lonlat

.. code:: ipython3

    folder = 'nrb_folder'
    filenames = sorted(os.listdir(folder))
    ds_sc = xr.open_zarr(os.path.join(folder, filenames[5]))
    ds_sc['sigma0'] = np.abs(ds_sc.v)
    ds_sc = reproj_lonlat(ds_sc)


.. parsed-literal::

    /data1/yyuan6/anaconda3/envs/harmony-ard-3.12/lib/python3.12/site-packages/rasterio/warp.py:387: ComplexWarning: Casting complex values to real discards the imaginary part
      dest = _reproject(


.. code:: ipython3

    # read in geometry information: platform heading and angle of incidence
    platform_angle = open_datatree('geometry_folder', 
                                    engine='zarr', chunks={}).cstack.attrs['SCPCOA']['AzimAng']
    theta_folder = 'angle_of_incidence_folder'
    ds_theta = xr.open_zarr(theta_folder)
    ds_theta = reproj_lonlat(ds_theta)
    ds_sc['theta'] = (['y', 'x'], np.degrees(ds_theta.v.data))

Bright target removal
---------------------

To identify the bright target statistically, the sigma0 is low-pass
filtered with a Gaussian window

.. math:: I^{\mathrm{LPF}}(x,y) = I(x,y)*h_{\mathrm{LP}}(x,y),

with

.. math:: h_{\mathrm{LP}}(x,y) = \frac{1}{\sigma_x\sigma_y\sqrt{2\pi}}e^{-\frac{x_{i}^{2}}{2\sigma_{x}^{2}}-\frac{y_{i}^{2}}{2\sigma_{y}^{2}}},

the impulse reponse of the Gaussian filter, where :math:`\sigma_{x,y}`
are the filter widths, which can be in the order of km. We then compute
the intensity contrast as

.. math:: K(x,y) = \frac{I(x,y) - I^{\mathrm{LPF}}(x,y)}{I^{\mathrm{LPF}}(x,y)}.

PIxels for which the intensity contrast exceeds a given threshold,

.. math:: K(x,y) >K_{\mathrm{thres}}

are considered outliers. Consequently, a mask is generated accroding to

.. math::

   M(x,y) = \begin{cases}
   1, & \text{if } K(x,y) < K_{\mathrm{thres}} \\
   0,  & \text{if } K(x,y) > K_{\mathrm{thres}}
   \end{cases}.

To define the constrat threshold, we assume the intensity distribution
of a single-look pixel is exponential, then the mean and standard
deviation of the intensity are equal to :math:`\frac{1}{\lambda}`. The
summation of multiple independent exponential distributions changes the
statistics. According to error propagation law, the mean and the
standard devaition is scaled with the number of independent samples, in
this case, the equivalent number of looks (ENL). The mean and the
standard deviation are

.. math:: \mu = \frac{\mathrm{ENL}}{\lambda}, \sigma = \frac{\sqrt{\mathrm{ENL}}}{\lambda}.

Therefore, the standard deviation can be written as a scaled mean

.. math:: \sigma = \frac{\mu}{\sqrt{\mathrm{ENL}}}.

Downsample
----------

After the outlier removal, the energy loss due to the mask is restored.
This is done by dividing the masked :math:`\sigma_0` by the low-pass
filtered mask. Then, the noise-floor is substracted.

.. math:: \sigma_{0,\mathrm{L}} = \frac{(I(x,y)\cdot M(x,y))*h_{\mathrm{LP}}(x,y)}{M(x,y)*h_{\mathrm{LP}}(x,y)}-\mathrm{NESZ}

After these steps, the downsample is performed by using the resolution
of the input data and the user desired resolution as input parameters.

Angle of incidence compensation
-------------------------------

This step takes ERA5 wind product and SAR geometry as inputs to predict
the NRCS using a L-band GMF. The angle of incidence compensation is
achived by scaling the downsampled product using the model output as
:math:`\sigma_{0,\mathrm{L}}/\sigma_{0,\mathrm{mod}}`.

.. code:: ipython3

    import cv2
    import xsar
    from pathlib import Path
    from dataclasses import dataclass
    from HARD.Model.L_GMF import lband_gmf
    from HARD.Processing.Utils.utils import dtype_conversion
    from HARD.Download.download_ERA5 import download_wind_for_S1
    from HARD.Processing.GRD_processing.subsample import subsample
    from HARD.Processing.Utils.utils_era5 import get_mean_wind_era5
    from HARD.Processing.Utils.utils_era5 import wdir_wrt_sensor_from_era5
    from HARD.Processing.GRD_processing.roughness import nrcs_to_roughness
    from HARD.Processing.GRD_processing.format_output import format_output
    from HARD.Processing.Compression.saving_compression import CompressionAccessor
    from HARD.Processing.GRD_processing.blurring import blur_2D_along_polarization, blur_2D
    
    
    class Process_SAOCOM_SLC(object):
        def __init__(self,dataset, platform_angle, enl, target_samp, pol, filename, era5_path):
            self.sigma_gau = 1
            self.pol = pol
            self.ground_heading = -180 + platform_angle - 90
            self.enl = enl
            self.nesz = 10**(-3)
            self.original_samp = 10
            self.target_samp = target_samp
            self.contrast_threshold = 3
            self.filename = filename
            self.ERA5_path = era5_path
            self.ds_xsar = dataset
            self.outlier_samp = 2500 #300
             # -- determine kernel size for mask generation
            self.win_size_mask = int(self.outlier_samp/self.original_samp + 1) # the width and height of the kernel which should be positive and odd
            self.sigmax_mask = (self.win_size_mask - 1) / (2 * self.sigma_gau)
            
            # -- determine kernel size for product filter
            self.win_size_prod = int(self.target_samp/self.original_samp + 1) # the width and height of the kernel which should be positive and odd
            self.sigmax_prod = (self.win_size_prod - 1) / (2 * self.sigma_gau)
            
            self.dx_supsamp = int(self.target_samp/self.original_samp)
            
    
        def outlier_removal(self, variable: str ='sigma0', dimensions_to_blur: list[int] = ["y", "x"], axis_polarization: int = 0):
    
            
            # -- first we obtain the mask from the co-pol data
            da = self.ds_xsar[variable].data
    
            blurred = cv2.GaussianBlur(da, ksize=(self.win_size_mask, self.win_size_mask), sigmaX=self.sigmax_mask)
    
            contrast = (da - blurred)/(blurred/np.sqrt(self.enl))
            contrast_mask = xr.where(contrast>self.contrast_threshold, 0, 1)    
            
            # -- then we blur the mask itself
            masked = contrast_mask.astype('float32')
            blurred_mask = cv2.GaussianBlur(masked, ksize=(self.win_size_prod, self.win_size_prod), sigmaX=self.sigmax_prod)
    
            # -- and apply it to both co-pol and cross-pol
            da_masked = contrast_mask*(da - self.nesz) 
            blurred_and_masked = cv2.GaussianBlur(da_masked, ksize=(self.win_size_prod, self.win_size_prod), sigmaX=self.sigmax_prod)
    
            outlier_removed = blurred_and_masked / blurred_mask
            
            return contrast_mask, outlier_removed
        
        def roughness_comp(self, ds_xsar_coarse, variable: str ='sigma0'):
            """
            Angle of incidence compensated roughness, using mean wind within the region of interest.
    
            Parameters
            ----------
            variable : str, optional
                The variable name in the dataset to process (default is 'sigma0').
    
            Returns
            -------
            Tuple 
                The angle of incidence compensated roughness (xr.DataArray) and the magintude of wind which is used in cmod5 model.
    
            Examples
            --------
            >>> process_grd = ProcessGRD(GRD_path='path/to/grd', target_samp=10)
            >>> roughness = process_grd.roughness_comp(variable='sigma0')
            >>> print(roughness)
            """
            wind_file = download_wind_for_S1(ds=ds_xsar_coarse,
                                             era5_path=self.ERA5_path,
                                             filename=self.filename) 
            
            era5_path = os.path.join(self.ERA5_path, wind_file) # NOTE The ERA5 file was downloaded here, make sure the name is the same for you
    
            wind_mag, wind_dir = get_mean_wind_era5(era5_path=era5_path)
            wdir_wrt_sensor = wdir_wrt_sensor_from_era5(wdir_era5=wind_dir, 
                                                        ground_dir=self.ground_heading)
            ref_nrcs = lband_gmf(wind_mag, wdir_wrt_sensor, ds_xsar_coarse['theta'], self.pol)
            roughness = ds_xsar_coarse[variable].data / ref_nrcs
            return roughness.astype(np.float32), wind_mag
    
    
        def subsample_dataset(self, dims=['y', 'x']):
            """
            Subsamples the dataset based on the provided dimensions.
    
            Parameters
            ----------
            dims : list, optional
                The dimensions to subsample (default is ['line', 'sample']).
    
            Returns
            -------
            xr.Dataset
                The subsampled dataset.
    
            Examples
            --------
            >>> process_grd = ProcessGRD(GRD_path='path/to/grd', target_samp=10)
            >>> subsampled_ds = process_grd.subsample_dataset(dims=['line', 'sample'])
            >>> print(subsampled_ds)
            """
            resample_dict = {dim: self.dx_supsamp for dim in dims}
            return subsample(self.ds_xsar, dims=resample_dict)
    
    
        def preprocess(self, roughness_on = False):
            """
            Performs preprocessing steps including outlier removal, angle of incidence compensated roughness computation (optional) and subsampling.
    
            Returns
            -------
            xr.Dataset
                The preprocessed dataset.
    
            Examples
            --------
            >>> process_grd = ProcessGRD(GRD_path='path/to/grd', target_samp=10)
            >>> preprocessed_ds = process_grd.preprocess()
            >>> print(preprocessed_ds)
            """
            # FIXME we need to save the outliers in a sparse array or something, meaning we need to deal with more outputs below
    
            variable = 'sigma0'
    
            # -- remove outliers and overwrite variable
            contrast_mask, outliers_removed = self.outlier_removal(variable=variable)
            self.mask = contrast_mask 
            variable_new = 'sigma0_of'
            self.ds_xsar[variable_new] = (['y', 'x'], outliers_removed)
    
            # -- update attributes
            process_str = f"Outlier removal with kernel_size: {self.win_size_mask}, sigma:{self.sigmax_mask} and contrast threshold: {self.contrast_threshold}"
            self.ds_xsar[variable_new].attrs['HARD'] = process_str
    
            # -- coarsen by subsampling
            ds_xsar_coarse = self.subsample_dataset()
            ds_xsar_coarse.attrs['HARD'] = f"Subsampled by factor {self.dx_supsamp} in range and azimuth"
            
            if roughness_on:
                # turn on the roughness computation
                # -- add angle of incidence compensated roughness
                roughness, wind_mag = self.roughness_comp(ds_xsar_coarse, variable=variable_new)
                ds_xsar_coarse['roughness'] = (['y', 'x'], roughness.data)
    
                # -- update attributes
                process_str = f"Angle of incidence compensated roughness with mean wind: {wind_mag:.2f} m/s"
                ds_xsar_coarse['roughness'].attrs['HARD'] = process_str
    
            return ds_xsar_coarse

.. code:: ipython3

    aoi_name = 'test_saocom'
    era5_path = os.path.join('era5_wind_folder', aoi_name)
    SLC = Process_SAOCOM_SLC(ds_sc, platform_angle, enl = 1, target_samp = 300, pol = 'VV', filename = filenames[5], era5_path = era5_path)

.. code:: ipython3

    processed = SLC.preprocess(roughness_on = True).persist()


.. parsed-literal::

    File already exists!
    There is some water


.. code:: ipython3

    sigma0_outlier = xr.where(SLC.mask==0, ds_sc['sigma0'].data, np.nan)  
