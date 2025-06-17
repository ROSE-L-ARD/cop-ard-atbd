.. _mlc_code:

=======
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


