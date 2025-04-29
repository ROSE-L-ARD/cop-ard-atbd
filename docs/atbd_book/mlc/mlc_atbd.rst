
.. _mlc_label:

=================================================
Algorithm Theoretical Basis Document (ATBD) - MLC
=================================================

Overview
===========

The MLC product is a multi-looked ARD product suited to large-scale interferometric applications. It is inspired by intermediate products which are normally present in PS/DS and SBAS chains before phase unwrapping. For the ROSE-L missions the proposed resolution of this product is 50 m. It is intended to simplify the access to interferometric measurements which are usually quite unaccessible: the product is intended to have reduced noise as it is already multilooked, it is generated with a mechanism to minimize long-term phase drifts related to vegetation effects, and it has a much smaller size compared to the original CSLC stack. The product is first generated in radar coordinates on a sub-sampling of the original SLC grid. Because of this, this version is called CMLC (Co-registered Multi-looked Complex). Its final version after geocoding is called GMLC.

There are different approaches in the literature to generate such product. Here we describe an algorithm which exhibits the following characteristics:

- it is very lightweight in terms of data I/O and computation,
- it enables continuous product update as new images are acquired and the CLSC stack grows,
- it incorporates a long-term drift correction.


Product Description
======================

The multi-looked phase consists of one layer for each acquisition date of the input CSLC products. We generate it originally in radar geometry and project it to the ground at the very end. Receiving the product in ground coordinates is important for many users. (Mosaicking should also be considered). The time series of MLC phases can be used to quickly obtain interferometric maps between tow dates or relative deformation time series between two or more points.

Some of the characteristics of this product are shared with the INT and GINT products. All model-driven and data driven corrections (atmosphere, solid earth tides, etc.) can be applied to this product, if they are not already included in the input CSLCs.

The target posting is 50 m, in line with the ROSE-L MRD. Advanced realizations could consider the use of adaptive multi-looking, either with older methods for homogeneous pixel selection or newer machine learning techniques. These are not considered at the moment.

This product includes two quality layers in the form of coherence. Quality layers can be very useful for the user for example to guide space/time phase unwrapping.

The GMLC ground grid is defined to ensure compatibility between missions and products.

Main variables
------------------

- **Wrapped multilooked phase** :math:`\phi_n`: This is a temporal collection of phase maps that can be used to generate multi-looked interferograms for any chosen pair of acquisitions in the stack, without having to start from full-resolution images. Taken singularly, each map represents conceptually the interferometric phase between each acquisition and a fixed reference (e.g. the first acquisition in the stack) that one could compute directly by forming an interferogram with the reference. In practice, the direct interferometric phase and the MLC phase will differ: the MLC phase should be less noisy.

- **Long-term coherence** :math:`\gamma^l_n`: This is a temporal collection of coherence maps that represents the long-term coherence of each acquisition with its past. This information can be useful as an indication of the noisiness of interferograms computed between acquisitions that are separated by a large time interval (e.g. 1 year or more). The exact interpretation depends on the chosen processing parameters.

- **Short-term coherence** :math:`\gamma^s_n`: This is a temporal collection of coherence maps that represents the short-term coherence of each acquisition with its recent past. This information can be useful as an indication of the noisiness of interferograms computed between acquisitions that are separated by a short time interval (e.g. a few weeks). The exact interpretation depends on the chosen processing parameters.

Metadata
------------

...

Input data
=============

SAR data
------------

The input for the generation of this product is a CSLC product, i.e. a stack of co-registered slc's in radar geometry. The algorithm is designed to work with continuous updates, so that it is not necessary to have access to the entire stack at each step, for each new incoming acquisition.

Internal data
-----------------

This algorithm keeps two special images between each update step, one is called "running reference" and the other "past reference". These images are linear combinations of images that have been already processed and are introduced to avoid accessing the entire past history.

Auxiliary data
------------------

...


Algorithm description
========================

.. figure:: ./images/CMLC_generation.png
   :name: Workflow for CMLC generation.
   :scale: 60%
   :align: center

   Workflow for CMLC generation.

Phase and short-term coherence estimation
---------------------------------------------

The multilooked phase is going to be generated by interfering each incoming CSLC acquisition :math:`y_n` with the current reference :math:`z_n` (a “running reference”) and averaging over a small pixel neighborhood :math:`\Omega`:

.. math::
    \phi_n = \angle \sum_{(r,a) \in \Omega} z_n^*(r,a) y_n(r,a).

In our implementation the neighborhood is simply a rectangular window.
At the very beginning, the reference :math:`z_n` is going to be initialized with the first image in the CSCL stack (i.e. :math:`z_1 = y_1`). Later it is going to be updated as described below.

The short-term coherence :math:`\gamma^s_n` is simply taken as the coherence of the same interferogram between :math:`y_n` and :math:`z_n` shown above.

Running reference update
-----------------------------
After the estimation of the interferometric phase :math:`\phi_n`, we are going to use it to update the running reference :math:`z_n` by including the contribution of the current CSLC :math:`y_n.`

.. math::
    z_{n+1} = \alpha z_n + y_n e^{-j\phi_n}.


The memory parameter :math:`\alpha` controls the bandwidth of the running reference, a small parameter corresponds to a short memory, which is optimal for fast-decorrelating scenarios. A large value of the parameter is suited to stable targets.

Running reference calibration
---------------------------------

As time passes, the running reference risks drifting away from the phase of the first acquisition of the stack. For this reason we are going to calibrate its phase with a more stable reference :math:`p` by generating an interferogram and compensating the phase:

.. math::
    \varphi = \angle \sum_{(r,a) \in \Omega} p_n^*(r,a) z_{n+1}(r,a).


.. math::
    z_{n+1} \leftarrow z_{n+1} e^{-j\varphi}.


The phase compensation is performed only if the coherence between :math:`p_n` and :math:`z_{n+1}` is above a chosen threshold (e.g. 0.1) to avoid adding noise in cases of low coherence.

Stable reference generation and update
------------------------------------------

We take initially a snapshot of the running reference :math:`z` as a stable reference :math:`p` after a certain number of update steps (e.g. :math:`m=10` which would correspond to 60 days for a 6-day repeat ROSE-L time series):

.. math::
    p_n = z_n, \quad \textrm{for} \quad n=m.

After that we update the stable reference with a pace with is slower than the pace we update the running reference, so that the stable reference represents older acquisitions.

.. math::
    p_{n+1} = \beta_1 p_n + \beta_2 z_n.

With the choice :math:`\beta = 1, \gamma=1` the stable reference is simply the sum of all past running references from step :math:`m` onwards. It represents therefore the mid-point between the current acquisition and the :math:`m^{th}` acquisition.

With the choice :math:`\gamma=0` the stable reference is not going to be updated with new information and remains frozen.


The long-term coherence :math:`\gamma^l_n` is taken as the coherence of the same interferogram between :math:`y_n` and :math:`p_n`.

Geocoding
-------------
* :ref:`GEOCODING <common_geocoding_label>`


Mosaicking
--------------
* :ref:`MOSAIC <common_mosaic_label>`


Algorithm improvement
=====================
- Better sampling in radar coordinates of CMLC product
- Saving and make use of several "past references", e.g. one for each year
- Adaptive parameter selection for the temporal filter, which should be coherence-dependent. This is not trivial as we are going to optimize simultaneously the short and the long-term coherence.


Data visualization
=====================

Interferogram generation in GIS software
--------------------------------------------

It is possible to generate interferograms directly in a GIS software. Once the zarr file is loaded, one needs only calling a "raster calculator" function operating on two chosen dates. 
For example in QGIS on can pick two rasters that correspond to the chose dates and take the phase difference

.. math::
    \phi = \phi_1 - \phi_2

and feed it to a function that realizes the two-argument arctangent by using only the common arctangent, sine, and cosine:

.. math::
    \varphi = \mathrm{atan2}\left(\sin(\phi), \cos(\phi)\right) = 2\:\mathrm{atan}\left(\frac{\sin(\phi)}{1+\cos(\phi)}\right)= 2\:\mathrm{atan}\left(\frac{1- \cos(\phi)}{\sin(\phi)}\right).


Code
=======

.. code-block:: python
    :caption: Import modules

    # import basic modules
    import zarr
    import numpy as np
    from tqdm import tqdm


.. code-block:: python
    :caption: basedir definition

    base_dir = "/media/data/SAR/L2/Naples/ASC/S4/"


.. code-block:: python
    :caption: parameter definition

    # selecting window sizes (rg, az) and mini_size (number of acquisitions after which the long-term calibration kicks-in)
    w_rg = 10
    w_az = 20
    mini_size = 10
    memory_param = 0.90 # autoregression parameter for the reference update (0 => totally forgetting the past)
    memory_param_past_beta1 = 0.95 # autor-egressive parameter for the past reference update (0 => totally forgetting the past)
    memory_param_past_beta2 = 1 # moving-average parameter for the past reference update
    coherence_threshold = 0.1 # threshold to calibrate current reference with a past reference (below that, skip calibration)

.. code-block:: python
    :caption: opening the CSLC dataset

    # opening the CSLC dataset
    ds = zarr.open(base_dir + "slcs.zarr")
    cstack = ds.coreg.cstack
    N = len(cstack)

.. code-block:: python
    :caption: parameters definition

    # choosing the indices of one window (normally we are going to iterate over all window indices)
    i_rg = 100
    i_az = 500

.. code-block:: python
    :caption: building indices to cut a slice for the selected window

    # building indices to cut a slice for the selected window
    rg_range = np.arange((i_rg-1)*w_rg+0,(i_rg)*w_rg+0)
    az_range = np.arange((i_az-1)*w_az+0,(i_az)*w_az+0)
    wnd_range = np.ix_(az_range, rg_range)

.. code-block:: python
    :caption: inizializing output arrays

    # inizializing output arrays
    interf = np.zeros(N, dtype=np.complex64)
    short_term_coherence = np.zeros(N)*np.nan
    long_term_coherence = np.zeros(N)*np.nan

.. code-block:: python
    :caption: basic function definition

    def make_interf(A, B):
        return np.conj(A).dot(B)

    def make_coh(A, B):
        return make_interf(A,B) / np.sqrt(make_interf(A,A) * make_interf(B,B))


.. code-block:: python
    :caption: main algorithm

    # main algorithm (progressive interferometric phase estimation)

    # initializing references (internal variables)
    #current_reference = cstack[0][wnd_range].ravel()
    current_reference = cstack[N-1][wnd_range].ravel()
    past_reference = np.zeros_like(current_reference)

    step = 0
    #for n in tqdm(range(0,N)):
    for n in tqdm(range(N-1,-1,-1)):
        step = step + 1
        slc = cstack[n][wnd_range].ravel()  # getting the current slc
        interf[n] = make_coh(current_reference,slc)
        short_term_coherence[n] = abs(interf[n])
        
        # updating the current reference
        current_reference = current_reference*memory_param + slc*np.conj(interf[n])

        # initializing the past reference
        if step == mini_size :
            past_reference[:] = current_reference
            
        # long-term phase calibration of current_reference
        if step > mini_size :
            corr_phase = make_coh(past_reference,current_reference)
            if np.abs(corr_phase) > coherence_threshold :
                current_reference[:] = current_reference * (np.conj(corr_phase)/np.abs(corr_phase))
                long_term_coherence[n] = np.abs(make_coh(past_reference,slc))
            past_reference = past_reference * memory_param_past_beta_1 + current_reference * memory_param_past_beta_2


Validation and Quality Assessment
=====================================

* Test 1
* Test 2


References
=============

.. bibliography::

Appendices
=============

* [Detailed mathematical derivations]