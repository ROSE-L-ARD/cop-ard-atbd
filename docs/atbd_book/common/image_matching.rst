.. _image_matching:

Image matching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Overview
--------

The purpose of this utilitiy is to compute the shift between a reference and a secondary image, by maximizing the module of the Pearson correlation coefficient.
In order to be robust with respect to phase decorrelation effects (long time series or large baselines), it is suggested to consider only the intensity of the image in the computation of the correlation coefficient.

Inputs
-------

- :math:`slc_r`: reference SLC image
- :math:`slc_s`: secondary SLC image

Outputs
--------

- :math:`(\delta t_{r_s},\delta t_{a_s})`: offset in slant range and azimuth directions to be applied to the secondary image to match the reference image
- :math:`\Gamma(\delta t_{r_s},\delta t_{a_s})`: Objective function in correspondence of the optimum shift


Algorithm
----------

The Pearson correlation coefficient between the reference image :math:`slc_r` and the secondary image :math:`slc_s` shifted of :math:`(\delta t_{r_s},\delta t_{a_s})` is defined as:

.. math::
    :label: eq_pearson

    \Gamma(\delta t_{r_s}, \delta t_{a_s}) = \left | \frac{E\left[ \text{slc}_r(t_{r_s}, t_{a_s}) \text{slc}_s^{*}(t_{r_s}+\delta t_{r_s}, t_{a_s}+\delta t_{a_s}) \right ]}{\sqrt{ E \left [ \left| \text{slc}_r(t_{r_s}, t_{a_s}) \right|^2 \right ] E \left [ \left| \text{slc}_s(t_{r_s}+\delta t_{r_s}, t_{a_s}+\delta t_{a_s}) \right|^2 \right ]}} \right | 

.. note::
    If the input reference and secondary images are complex-valued, it is important that the phase modulation due to the acquisition mode and acquisition geometry (topography) has been removed.

To find the values :math:`(\delta t_{r_s}, \delta t_{a_s})` that maximize the function :math:`\Gamma(\delta t_{r_s}, \delta t_{a_s})` with sub-pixel accuracy, it is sufficient to evaluate the function at offsets that are integer multiples of the image spacing. Once the function has been computed at these integer nodes, it is possible to oversample the objective function or fit a paraboloid around the local peak to obtain the coordinates of the maximum.
The maximum of the objevtive function and the position of the maximum are the main outputs of the function.


Code
-------

.. code-block::

    def compute_pearson_coefficient(
        stack: xr.DataArray,
        ref_date: str,
        mode: Literal["amplitude", "complex"] = "amplitude",
        wsearch: Sequence[int] | None = None,
        forward: bool = True,
        dim: Sequence[int] | None = None,
        type: Literal["times", "pixels"] = "pixels",
        chunk: dict | None = None,
        job_id: int | None = None,
    ) -> np.ndarray:
        """Compute the maximum of the Pearson correlation
        coefficient of a stack of images w.r.t a reference image

        where i1 and i2 are 0 mean and norm 1 vectors

        The reference image is one of the images of the stack with index "ref"
        The maximization is performed considering a window

        """
        # check output type #
        assert type in ["times", "pixels"], f"Invalid output type {type}"

        # check that the reference image is part of the stack
        acquisition_date = stack.acquisition_date.values
        assert ref_date in acquisition_date, f"Reference date {ref_date} not found into the input stack"
        ([index],) = np.where(acquisition_date == ref_date)

        if type == "times":
            # patch center and spacing expressed in times #
            pixel_to_time = np.array(
                [
                    [stack.RMA["INCA"]["TimeCAPoly"]["Coefs"][1] * stack.Grid["Col"]["SS"] * 1e9],
                    [2 * stack.Grid["Row"]["SS"] / speed_of_light],
                ],
                dtype="float64",
            )
            loc = [stack[e].mean().values for e in ["azimuth_time", "slant_range_time"]]  # da sistemare ####
        else:
            # patch center and spacing expressed in pixels #
            pixel_to_time = np.ones((2, 1), dtype="float32")
            if chunk is not None:
                loc = [(chunk[e].start + chunk[e].stop - 1) / 2 for e in ["azimuth_time", "slant_range_time"]]
            else:
                loc = [0, 0]

        stack = stack.transpose("azimuth_time", "slant_range_time", "acquisition_date").values
        if mode == "amplitude":
            stack = np.abs(stack)

        # define search window if not defined
        if wsearch is None:
            wsearch = list(np.array(stack.shape[0:2]) // 4)

        if isinstance(wsearch, int):
            wsearch = [wsearch, wsearch]

        # number of points of each image used to evaluate the Pearson correlation coefficient
        shp = np.array(stack.shape[0:2]) - 2 * np.array(wsearch)

        # number of images
        nim = stack.shape[2]

        # number of points of each image
        npt = shp[0] * shp[1]

        # correlation window dimension
        nco = (2 * wsearch[0] + 1) * (2 * wsearch[1] + 1)

        if forward:
            """
            i1                      i2

                    |  0  |                     |  0  |  1  | ...... |  npt-1  |
            --------|-----|         ------------|-----|-----|        |---------|
            p(0)    |     |         0           |     |     |        |         |
            --------|-----|         ------------|-----|-----|        |---------|
            p(1)    |     |         1           |     |     |        |         |
            --------|-----|         ------------|-----|-----|        |---------|
            p(2)    |     |         2           |     |     |        |         |
            --------|-----|         ------------|-----|-----|        |---------|
            .       |     |         .           |     |     |        |         |
            .       |     |         .           |     |     |        |         |
            .       |     |         .           |     |     |        |         |
            --------|-----|         ------------|-----|-----|        |---------|
            p(npt-1)|     |         nco x nim -1|     |     |        |         |
            --------|-----|         ------------|-----|-----|        |---------|
            """
            i1 = np.empty((npt, 1), dtype=stack.dtype)
            i2 = np.empty((nco * nim, npt), dtype=stack.dtype)

            # flatten reference image
            i1[:, 0] = stack[
                wsearch[0] : (-wsearch[0] if wsearch[0] > 0 else None),
                wsearch[1] : (-wsearch[1] if wsearch[1] > 0 else None),
                index,
            ].ravel()

            # flatten secondary images
            for i_z in range(stack.shape[2]):
                for count in range(nco):
                    i_y = count // (2 * wsearch[1] + 1)
                    i_x = count % (2 * wsearch[1] + 1)
                    i2[count + i_z * nco, :] = stack[i_y : i_y + shp[0], i_x : i_x + shp[1], i_z].ravel()
        else:
            i1 = np.empty((npt, nco), dtype=stack.dtype)
            i2 = np.empty((nim, npt), dtype=stack.dtype)

            # flatten secondary images
            for count in range(nco):
                i_y = count // (2 * wsearch[1] + 1)
                i_x = count % (2 * wsearch[1] + 1)
                i1[:, count] = stack[i_y : i_y + shp[0], i_x : i_x + shp[1], index].ravel()

            # flatten reference image
            for i_z in range(stack.shape[2]):
                i2[i_z, :] = stack[
                    wsearch[0] : (-wsearch[0] if wsearch[0] > 0 else None),
                    wsearch[1] : (-wsearch[1] if wsearch[1] > 0 else None),
                    i_z,
                ].ravel()

        # remove bias
        i1 = i1 - i1.mean(axis=0)
        i2 = i2 - i2.mean(axis=1)[..., None]

        # scale to norm 1
        i1 = i1 / np.linalg.norm(i1, axis=0)
        i2 = i2 / np.linalg.norm(i2, axis=1)[..., None]

        # compute Pearson correlation coefficient
        corr = np.abs(i2 @ i1.conj())
        corr = corr.reshape([nim, 2 * wsearch[0] + 1, 2 * wsearch[1] + 1])

        dy, dx, cohe, sy, sx = get_corr_sub_pix(corr, dim).T
        return xr.DataArray(
            data=np.vstack((*np.vstack((dy, dx)) * pixel_to_time, cohe, sy, sx)).T.reshape(nim, -1, 5),
            dims=["acquisition_date", "point", "variable"],
            coords={
                "acquisition_date": acquisition_date,
                "point": [job_id],
                "y": (["point"], loc[:1]),
                "x": (["point"], loc[1:]),
                "variable": ["dy", "dx", "cohe", "s_y", "s_x"],
            },
            attrs={"type": type, "pixel_to_time": pixel_to_time.flatten()},
        )
