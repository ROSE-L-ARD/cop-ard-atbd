Visualization
=============

.. code:: ipython3

    import cartopy
    import matplotlib as mpl
    from cartopy import config
    import cartopy.crs as ccrs
    import scipy.stats as stats
    from matplotlib import colors
    from matplotlib import ticker
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    import matplotlib.patches as patches
    from cartopy.io.shapereader import Reader
    from cartopy.feature import ShapelyFeature
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

.. code:: ipython3

    def vis_area(lat, lon, data, vmin, vmax, cmap, lable_name, fig_name):
        plt.style.use('ieee')
        fig = plt.figure(figsize=(7, 4))
        img_extent = [-5.4, -4.3, 48.05, 48.8]
        ax = plt.axes(projection=ccrs.Mercator())
        ax.set_extent(img_extent, ccrs.PlateCarree())
        draw_labels = True
        gl = ax.gridlines(crs=ccrs.PlateCarree(), color='gray', draw_labels=draw_labels)
        xlabels_top=False
        xlabels_bottom=True
        ylabels_left=False
        ylabels_right=True
        if draw_labels:
            gl.top_labels = xlabels_top
            gl.left_labels = ylabels_left
            gl.bottom_labels = xlabels_bottom
            gl.right_labels = ylabels_right
            gl.xlines = True
            gl.ylines = True
            gl.xformatter = LONGITUDE_FORMATTER
            gl.yformatter = LATITUDE_FORMATTER
            gl.xlabel_style = {'size': 10}
            gl.ylabel_style = {'size': 10}
        land_10m = cartopy.feature.NaturalEarthFeature('physical', 'land', '10m',
                                                       edgecolor='face',
                                                       facecolor=cartopy.feature.COLORS['land'])
    
        ax.add_feature(land_10m, zorder=3)
    
        im = ax.pcolormesh(lon, lat, data, transform=ccrs.PlateCarree(), zorder=1, vmin=vmin, vmax=vmax, cmap=cmap)
        cbar_ax = fig.add_axes([0.18, 0.082, 0.03, 0.89])
        clb = fig.colorbar(im, cax=cbar_ax, extend='both')
        clb.set_label(label=lable_name, fontsize=10, labelpad=-4, y=1.1, rotation=0)
        clb.ax.yaxis.set_ticks_position('left')
        plt.tight_layout()
        plt.savefig(fig_name, transparent=False, bbox_inches='tight')

.. code:: ipython3

    vis_area(lat, lon, sigma0, 
             vmin=0, vmax=0.15, cmap='bone', lable_name = '$\sigma_{r,VV}$', 
             fig_name = 'sigma_raw.png')
    vis_area(lat, lon, sigma0_of, 
             vmin=0, vmax=0.15, cmap='bone', lable_name = '$\sigma_{VV}$', 
             fig_name = 'sigma0_L.png')
    vis_area(lat, lon, roughness, 
             vmin=0, vmax=1, cmap='bone', lable_name = '$\sigma_{VV}/\sigma_\mathrm{GMF_{L}@13.78 m/s}$', 
             fig_name = 'roughness.png')



.. image:: orb_data_vis_files/orb_data_vis_3_1.png


.. image:: orb_data_vis_files/orb_data_vis_3_3.png


.. image:: orb_data_vis_files/orb_data_vis_3_5.png


