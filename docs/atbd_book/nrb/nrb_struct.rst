
.. raw:: html

    <div><svg style="position: absolute; width: 0; height: 0; overflow: hidden">
    <defs>
    <symbol id="icon-database" viewBox="0 0 32 32">
    <path d="M16 0c-8.837 0-16 2.239-16 5v4c0 2.761 7.163 5 16 5s16-2.239 16-5v-4c0-2.761-7.163-5-16-5z"></path>
    <path d="M16 17c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
    <path d="M16 26c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
    </symbol>
    <symbol id="icon-file-text2" viewBox="0 0 32 32">
    <path d="M28.681 7.159c-0.694-0.947-1.662-2.053-2.724-3.116s-2.169-2.030-3.116-2.724c-1.612-1.182-2.393-1.319-2.841-1.319h-15.5c-1.378 0-2.5 1.121-2.5 2.5v27c0 1.378 1.122 2.5 2.5 2.5h23c1.378 0 2.5-1.122 2.5-2.5v-19.5c0-0.448-0.137-1.23-1.319-2.841zM24.543 5.457c0.959 0.959 1.712 1.825 2.268 2.543h-4.811v-4.811c0.718 0.556 1.584 1.309 2.543 2.268zM28 29.5c0 0.271-0.229 0.5-0.5 0.5h-23c-0.271 0-0.5-0.229-0.5-0.5v-27c0-0.271 0.229-0.5 0.5-0.5 0 0 15.499-0 15.5 0v7c0 0.552 0.448 1 1 1h7v19.5z"></path>
    <path d="M23 26h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
    <path d="M23 22h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
    <path d="M23 18h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
    </symbol>
    </defs>
    </svg>
    <style>/* CSS stylesheet for displaying xarray objects in jupyterlab.
     *
     */
    
    :root {
      --xr-font-color0: var(--jp-content-font-color0, rgba(0, 0, 0, 1));
      --xr-font-color2: var(--jp-content-font-color2, rgba(0, 0, 0, 0.54));
      --xr-font-color3: var(--jp-content-font-color3, rgba(0, 0, 0, 0.38));
      --xr-border-color: var(--jp-border-color2, #e0e0e0);
      --xr-disabled-color: var(--jp-layout-color3, #bdbdbd);
      --xr-background-color: var(--jp-layout-color0, white);
      --xr-background-color-row-even: var(--jp-layout-color1, white);
      --xr-background-color-row-odd: var(--jp-layout-color2, #eeeeee);
    }
    
    html[theme="dark"],
    html[data-theme="dark"],
    body[data-theme="dark"],
    body.vscode-dark {
      --xr-font-color0: rgba(255, 255, 255, 1);
      --xr-font-color2: rgba(255, 255, 255, 0.54);
      --xr-font-color3: rgba(255, 255, 255, 0.38);
      --xr-border-color: #1f1f1f;
      --xr-disabled-color: #515151;
      --xr-background-color: #111111;
      --xr-background-color-row-even: #111111;
      --xr-background-color-row-odd: #313131;
    }
    
    .xr-wrap {
      display: block !important;
      min-width: 300px;
      max-width: 700px;
    }
    
    .xr-text-repr-fallback {
      /* fallback to plain text repr when CSS is not injected (untrusted notebook) */
      display: none;
    }
    
    .xr-header {
      padding-top: 6px;
      padding-bottom: 6px;
      margin-bottom: 4px;
      border-bottom: solid 1px var(--xr-border-color);
    }
    
    .xr-header > div,
    .xr-header > ul {
      display: inline;
      margin-top: 0;
      margin-bottom: 0;
    }
    
    .xr-obj-type,
    .xr-array-name {
      margin-left: 2px;
      margin-right: 10px;
    }
    
    .xr-obj-type {
      color: var(--xr-font-color2);
    }
    
    .xr-sections {
      padding-left: 0 !important;
      display: grid;
      grid-template-columns: 150px auto auto 1fr 0 20px 0 20px;
    }
    
    .xr-section-item {
      display: contents;
    }
    
    .xr-section-item input {
      display: inline-block;
      opacity: 0;
      height: 0;
    }
    
    .xr-section-item input + label {
      color: var(--xr-disabled-color);
    }
    
    .xr-section-item input:enabled + label {
      cursor: pointer;
      color: var(--xr-font-color2);
    }
    
    .xr-section-item input:focus + label {
      border: 2px solid var(--xr-font-color0);
    }
    
    .xr-section-item input:enabled + label:hover {
      color: var(--xr-font-color0);
    }
    
    .xr-section-summary {
      grid-column: 1;
      color: var(--xr-font-color2);
      font-weight: 500;
    }
    
    .xr-section-summary > span {
      display: inline-block;
      padding-left: 0.5em;
    }
    
    .xr-section-summary-in:disabled + label {
      color: var(--xr-font-color2);
    }
    
    .xr-section-summary-in + label:before {
      display: inline-block;
      content: "►";
      font-size: 11px;
      width: 15px;
      text-align: center;
    }
    
    .xr-section-summary-in:disabled + label:before {
      color: var(--xr-disabled-color);
    }
    
    .xr-section-summary-in:checked + label:before {
      content: "▼";
    }
    
    .xr-section-summary-in:checked + label > span {
      display: none;
    }
    
    .xr-section-summary,
    .xr-section-inline-details {
      padding-top: 4px;
      padding-bottom: 4px;
    }
    
    .xr-section-inline-details {
      grid-column: 2 / -1;
    }
    
    .xr-section-details {
      display: none;
      grid-column: 1 / -1;
      margin-bottom: 5px;
    }
    
    .xr-section-summary-in:checked ~ .xr-section-details {
      display: contents;
    }
    
    .xr-array-wrap {
      grid-column: 1 / -1;
      display: grid;
      grid-template-columns: 20px auto;
    }
    
    .xr-array-wrap > label {
      grid-column: 1;
      vertical-align: top;
    }
    
    .xr-preview {
      color: var(--xr-font-color3);
    }
    
    .xr-array-preview,
    .xr-array-data {
      padding: 0 5px !important;
      grid-column: 2;
    }
    
    .xr-array-data,
    .xr-array-in:checked ~ .xr-array-preview {
      display: none;
    }
    
    .xr-array-in:checked ~ .xr-array-data,
    .xr-array-preview {
      display: inline-block;
    }
    
    .xr-dim-list {
      display: inline-block !important;
      list-style: none;
      padding: 0 !important;
      margin: 0;
    }
    
    .xr-dim-list li {
      display: inline-block;
      padding: 0;
      margin: 0;
    }
    
    .xr-dim-list:before {
      content: "(";
    }
    
    .xr-dim-list:after {
      content: ")";
    }
    
    .xr-dim-list li:not(:last-child):after {
      content: ",";
      padding-right: 5px;
    }
    
    .xr-has-index {
      font-weight: bold;
    }
    
    .xr-var-list,
    .xr-var-item {
      display: contents;
    }
    
    .xr-var-item > div,
    .xr-var-item label,
    .xr-var-item > .xr-var-name span {
      background-color: var(--xr-background-color-row-even);
      margin-bottom: 0;
    }
    
    .xr-var-item > .xr-var-name:hover span {
      padding-right: 5px;
    }
    
    .xr-var-list > li:nth-child(odd) > div,
    .xr-var-list > li:nth-child(odd) > label,
    .xr-var-list > li:nth-child(odd) > .xr-var-name span {
      background-color: var(--xr-background-color-row-odd);
    }
    
    .xr-var-name {
      grid-column: 1;
    }
    
    .xr-var-dims {
      grid-column: 2;
    }
    
    .xr-var-dtype {
      grid-column: 3;
      text-align: right;
      color: var(--xr-font-color2);
    }
    
    .xr-var-preview {
      grid-column: 4;
    }
    
    .xr-index-preview {
      grid-column: 2 / 5;
      color: var(--xr-font-color2);
    }
    
    .xr-var-name,
    .xr-var-dims,
    .xr-var-dtype,
    .xr-preview,
    .xr-attrs dt {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      padding-right: 10px;
    }
    
    .xr-var-name:hover,
    .xr-var-dims:hover,
    .xr-var-dtype:hover,
    .xr-attrs dt:hover {
      overflow: visible;
      width: auto;
      z-index: 1;
    }
    
    .xr-var-attrs,
    .xr-var-data,
    .xr-index-data {
      display: none;
      background-color: var(--xr-background-color) !important;
      padding-bottom: 5px !important;
    }
    
    .xr-var-attrs-in:checked ~ .xr-var-attrs,
    .xr-var-data-in:checked ~ .xr-var-data,
    .xr-index-data-in:checked ~ .xr-index-data {
      display: block;
    }
    
    .xr-var-data > table {
      float: right;
    }
    
    .xr-var-name span,
    .xr-var-data,
    .xr-index-name div,
    .xr-index-data,
    .xr-attrs {
      padding-left: 25px !important;
    }
    
    .xr-attrs,
    .xr-var-attrs,
    .xr-var-data,
    .xr-index-data {
      grid-column: 1 / -1;
    }
    
    dl.xr-attrs {
      padding: 0;
      margin: 0;
      display: grid;
      grid-template-columns: 125px auto;
    }
    
    .xr-attrs dt,
    .xr-attrs dd {
      padding: 0;
      margin: 0;
      float: left;
      padding-right: 10px;
      width: auto;
    }
    
    .xr-attrs dt {
      font-weight: normal;
      grid-column: 1;
    }
    
    .xr-attrs dt:hover span {
      display: inline-block;
      background: var(--xr-background-color);
      padding-right: 10px;
    }
    
    .xr-attrs dd {
      grid-column: 2;
      white-space: pre-wrap;
      word-break: break-all;
    }
    
    .xr-icon-database,
    .xr-icon-file-text2,
    .xr-no-icon {
      display: inline-block;
      vertical-align: middle;
      width: 1em;
      height: 1.5em !important;
      stroke-width: 0;
      stroke: currentColor;
      fill: currentColor;
    }
    </style><pre class='xr-text-repr-fallback'>&lt;xarray.Dataset&gt; Size: 1GB
    Dimensions:                (x: 8139, y: 10248)
    Coordinates:
      * x                      (x) float64 65kB 4.225e+05 4.225e+05 ... 5.039e+05
      * y                      (y) float64 82kB 4.574e+06 4.574e+06 ... 4.471e+06
        spatial_ref            int64 8B 0
    Data variables:
        gamma0                 (y, x) float32 334MB dask.array&lt;chunksize=(256, 256), meta=np.ndarray&gt;
        nlooks                 (y, x) float32 334MB dask.array&lt;chunksize=(256, 256), meta=np.ndarray&gt;
        local_incidence_angle  (y, x) float32 334MB dask.array&lt;chunksize=(256, 256), meta=np.ndarray&gt;</pre><div class='xr-wrap' style='display:none'><div class='xr-header'><div class='xr-obj-type'>xarray.Dataset</div></div><ul class='xr-sections'><li class='xr-section-item'><input id='section-c7dea2b5-00a2-4b75-9627-55fe4f18478d' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-c7dea2b5-00a2-4b75-9627-55fe4f18478d' class='xr-section-summary'  title='Expand/collapse section'>Dimensions:</label><div class='xr-section-inline-details'><ul class='xr-dim-list'><li><span class='xr-has-index'>x</span>: 8139</li><li><span class='xr-has-index'>y</span>: 10248</li></ul></div><div class='xr-section-details'></div></li><li class='xr-section-item'><input id='section-60199292-6c14-4d31-adf2-a129c16c0bbd' class='xr-section-summary-in' type='checkbox'  checked><label for='section-60199292-6c14-4d31-adf2-a129c16c0bbd' class='xr-section-summary' >Coordinates: <span>(3)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>x</span></div><div class='xr-var-dims'>(x)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>4.225e+05 4.225e+05 ... 5.039e+05</div><input id='attrs-564decf0-05b6-4f1c-a586-d4f341971eb8' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-564decf0-05b6-4f1c-a586-d4f341971eb8' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-6ef460ac-f8a6-494a-aca8-42a56670a734' class='xr-var-data-in' type='checkbox'><label for='data-6ef460ac-f8a6-494a-aca8-42a56670a734' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([422525., 422535., 422545., ..., 503885., 503895., 503905.],
          shape=(8139,))</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>y</span></div><div class='xr-var-dims'>(y)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>4.574e+06 4.574e+06 ... 4.471e+06</div><input id='attrs-8e58c032-d06e-4d41-89bd-1a27ba043522' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-8e58c032-d06e-4d41-89bd-1a27ba043522' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-014e4a33-097d-4399-8c44-3ffe2770569f' class='xr-var-data-in' type='checkbox'><label for='data-014e4a33-097d-4399-8c44-3ffe2770569f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([4573845., 4573835., 4573825., ..., 4471395., 4471385., 4471375.],
          shape=(10248,))</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>spatial_ref</span></div><div class='xr-var-dims'>()</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-3e0c4a1e-e7db-49c2-8868-3d7e2ddf7fd1' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-3e0c4a1e-e7db-49c2-8868-3d7e2ddf7fd1' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a9f47e8c-784e-4138-b2ce-7f60a17f4a71' class='xr-var-data-in' type='checkbox'><label for='data-a9f47e8c-784e-4138-b2ce-7f60a17f4a71' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>crs_wkt :</span></dt><dd>PROJCS[&quot;WGS 84 / UTM zone 33N&quot;,GEOGCS[&quot;WGS 84&quot;,DATUM[&quot;WGS_1984&quot;,SPHEROID[&quot;WGS 84&quot;,6378137,298.257223563,AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],PRIMEM[&quot;Greenwich&quot;,0,AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],UNIT[&quot;degree&quot;,0.0174532925199433,AUTHORITY[&quot;EPSG&quot;,&quot;9122&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]],PROJECTION[&quot;Transverse_Mercator&quot;],PARAMETER[&quot;latitude_of_origin&quot;,0],PARAMETER[&quot;central_meridian&quot;,15],PARAMETER[&quot;scale_factor&quot;,0.9996],PARAMETER[&quot;false_easting&quot;,500000],PARAMETER[&quot;false_northing&quot;,0],UNIT[&quot;metre&quot;,1,AUTHORITY[&quot;EPSG&quot;,&quot;9001&quot;]],AXIS[&quot;Easting&quot;,EAST],AXIS[&quot;Northing&quot;,NORTH],AUTHORITY[&quot;EPSG&quot;,&quot;32633&quot;]]</dd><dt><span>semi_major_axis :</span></dt><dd>6378137.0</dd><dt><span>semi_minor_axis :</span></dt><dd>6356752.314245179</dd><dt><span>inverse_flattening :</span></dt><dd>298.257223563</dd><dt><span>reference_ellipsoid_name :</span></dt><dd>WGS 84</dd><dt><span>longitude_of_prime_meridian :</span></dt><dd>0.0</dd><dt><span>prime_meridian_name :</span></dt><dd>Greenwich</dd><dt><span>geographic_crs_name :</span></dt><dd>WGS 84</dd><dt><span>horizontal_datum_name :</span></dt><dd>World Geodetic System 1984</dd><dt><span>projected_crs_name :</span></dt><dd>WGS 84 / UTM zone 33N</dd><dt><span>grid_mapping_name :</span></dt><dd>transverse_mercator</dd><dt><span>latitude_of_projection_origin :</span></dt><dd>0.0</dd><dt><span>longitude_of_central_meridian :</span></dt><dd>15.0</dd><dt><span>false_easting :</span></dt><dd>500000.0</dd><dt><span>false_northing :</span></dt><dd>0.0</dd><dt><span>scale_factor_at_central_meridian :</span></dt><dd>0.9996</dd><dt><span>spatial_ref :</span></dt><dd>PROJCS[&quot;WGS 84 / UTM zone 33N&quot;,GEOGCS[&quot;WGS 84&quot;,DATUM[&quot;WGS_1984&quot;,SPHEROID[&quot;WGS 84&quot;,6378137,298.257223563,AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],PRIMEM[&quot;Greenwich&quot;,0,AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],UNIT[&quot;degree&quot;,0.0174532925199433,AUTHORITY[&quot;EPSG&quot;,&quot;9122&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]],PROJECTION[&quot;Transverse_Mercator&quot;],PARAMETER[&quot;latitude_of_origin&quot;,0],PARAMETER[&quot;central_meridian&quot;,15],PARAMETER[&quot;scale_factor&quot;,0.9996],PARAMETER[&quot;false_easting&quot;,500000],PARAMETER[&quot;false_northing&quot;,0],UNIT[&quot;metre&quot;,1,AUTHORITY[&quot;EPSG&quot;,&quot;9001&quot;]],AXIS[&quot;Easting&quot;,EAST],AXIS[&quot;Northing&quot;,NORTH],AUTHORITY[&quot;EPSG&quot;,&quot;32633&quot;]]</dd></dl></div><div class='xr-var-data'><pre>array(0)</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-c33d95d8-4024-41a6-b433-2f3d57cb2489' class='xr-section-summary-in' type='checkbox'  checked><label for='section-c33d95d8-4024-41a6-b433-2f3d57cb2489' class='xr-section-summary' >Data variables: <span>(3)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span>gamma0</span></div><div class='xr-var-dims'>(y, x)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>dask.array&lt;chunksize=(256, 256), meta=np.ndarray&gt;</div><input id='attrs-155dd791-1084-4ed8-85d3-18026281a31a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-155dd791-1084-4ed8-85d3-18026281a31a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-af35ea8d-bdf2-41b6-956b-64851ad26cb4' class='xr-var-data-in' type='checkbox'><label for='data-af35ea8d-bdf2-41b6-956b-64851ad26cb4' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><table>
        <tr>
            <td>
                <table style="border-collapse: collapse;">
                    <thead>
                        <tr>
                            <td> </td>
                            <th> Array </th>
                            <th> Chunk </th>
                        </tr>
                    </thead>
                    <tbody>
    
                        <tr>
                            <th> Bytes </th>
                            <td> 318.18 MiB </td>
                            <td> 256.00 kiB </td>
                        </tr>
    
                        <tr>
                            <th> Shape </th>
                            <td> (10248, 8139) </td>
                            <td> (256, 256) </td>
                        </tr>
                        <tr>
                            <th> Dask graph </th>
                            <td colspan="2"> 1312 chunks in 3 graph layers </td>
                        </tr>
                        <tr>
                            <th> Data type </th>
                            <td colspan="2"> float32 numpy.ndarray </td>
                        </tr>
                    </tbody>
                </table>
            </td>
            <td>
            <svg width="145" height="170" style="stroke:rgb(0,0,0);stroke-width:1" >
    
      <!-- Horizontal lines -->
      <line x1="0" y1="0" x2="95" y2="0" style="stroke-width:2" />
      <line x1="0" y1="5" x2="95" y2="5" />
      <line x1="0" y1="11" x2="95" y2="11" />
      <line x1="0" y1="17" x2="95" y2="17" />
      <line x1="0" y1="23" x2="95" y2="23" />
      <line x1="0" y1="29" x2="95" y2="29" />
      <line x1="0" y1="35" x2="95" y2="35" />
      <line x1="0" y1="44" x2="95" y2="44" />
      <line x1="0" y1="50" x2="95" y2="50" />
      <line x1="0" y1="56" x2="95" y2="56" />
      <line x1="0" y1="62" x2="95" y2="62" />
      <line x1="0" y1="68" x2="95" y2="68" />
      <line x1="0" y1="74" x2="95" y2="74" />
      <line x1="0" y1="83" x2="95" y2="83" />
      <line x1="0" y1="89" x2="95" y2="89" />
      <line x1="0" y1="95" x2="95" y2="95" />
      <line x1="0" y1="101" x2="95" y2="101" />
      <line x1="0" y1="107" x2="95" y2="107" />
      <line x1="0" y1="113" x2="95" y2="113" />
      <line x1="0" y1="120" x2="95" y2="120" style="stroke-width:2" />
    
      <!-- Vertical lines -->
      <line x1="0" y1="0" x2="0" y2="120" style="stroke-width:2" />
      <line x1="2" y1="0" x2="2" y2="120" />
      <line x1="8" y1="0" x2="8" y2="120" />
      <line x1="14" y1="0" x2="14" y2="120" />
      <line x1="17" y1="0" x2="17" y2="120" />
      <line x1="23" y1="0" x2="23" y2="120" />
      <line x1="29" y1="0" x2="29" y2="120" />
      <line x1="32" y1="0" x2="32" y2="120" />
      <line x1="38" y1="0" x2="38" y2="120" />
      <line x1="44" y1="0" x2="44" y2="120" />
      <line x1="47" y1="0" x2="47" y2="120" />
      <line x1="53" y1="0" x2="53" y2="120" />
      <line x1="59" y1="0" x2="59" y2="120" />
      <line x1="62" y1="0" x2="62" y2="120" />
      <line x1="68" y1="0" x2="68" y2="120" />
      <line x1="74" y1="0" x2="74" y2="120" />
      <line x1="77" y1="0" x2="77" y2="120" />
      <line x1="83" y1="0" x2="83" y2="120" />
      <line x1="89" y1="0" x2="89" y2="120" />
      <line x1="95" y1="0" x2="95" y2="120" style="stroke-width:2" />
    
      <!-- Colored Rectangle -->
      <polygon points="0.0,0.0 95.30444964871195,0.0 95.30444964871195,120.0 0.0,120.0" style="fill:#8B4903A0;stroke-width:0"/>
    
      <!-- Text -->
      <text x="47.652225" y="140.000000" font-size="1.0rem" font-weight="100" text-anchor="middle" >8139</text>
      <text x="115.304450" y="60.000000" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(-90,115.304450,60.000000)">10248</text>
    </svg>
            </td>
        </tr>
    </table></div></li><li class='xr-var-item'><div class='xr-var-name'><span>nlooks</span></div><div class='xr-var-dims'>(y, x)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>dask.array&lt;chunksize=(256, 256), meta=np.ndarray&gt;</div><input id='attrs-b1050233-85ef-4514-850e-d155e399ff4a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-b1050233-85ef-4514-850e-d155e399ff4a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-24cf7884-a271-4266-88e5-a4ec6f850fb9' class='xr-var-data-in' type='checkbox'><label for='data-24cf7884-a271-4266-88e5-a4ec6f850fb9' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><table>
        <tr>
            <td>
                <table style="border-collapse: collapse;">
                    <thead>
                        <tr>
                            <td> </td>
                            <th> Array </th>
                            <th> Chunk </th>
                        </tr>
                    </thead>
                    <tbody>
    
                        <tr>
                            <th> Bytes </th>
                            <td> 318.18 MiB </td>
                            <td> 256.00 kiB </td>
                        </tr>
    
                        <tr>
                            <th> Shape </th>
                            <td> (10248, 8139) </td>
                            <td> (256, 256) </td>
                        </tr>
                        <tr>
                            <th> Dask graph </th>
                            <td colspan="2"> 1312 chunks in 2 graph layers </td>
                        </tr>
                        <tr>
                            <th> Data type </th>
                            <td colspan="2"> float32 numpy.ndarray </td>
                        </tr>
                    </tbody>
                </table>
            </td>
            <td>
            <svg width="145" height="170" style="stroke:rgb(0,0,0);stroke-width:1" >
    
      <!-- Horizontal lines -->
      <line x1="0" y1="0" x2="95" y2="0" style="stroke-width:2" />
      <line x1="0" y1="5" x2="95" y2="5" />
      <line x1="0" y1="11" x2="95" y2="11" />
      <line x1="0" y1="17" x2="95" y2="17" />
      <line x1="0" y1="23" x2="95" y2="23" />
      <line x1="0" y1="29" x2="95" y2="29" />
      <line x1="0" y1="35" x2="95" y2="35" />
      <line x1="0" y1="44" x2="95" y2="44" />
      <line x1="0" y1="50" x2="95" y2="50" />
      <line x1="0" y1="56" x2="95" y2="56" />
      <line x1="0" y1="62" x2="95" y2="62" />
      <line x1="0" y1="68" x2="95" y2="68" />
      <line x1="0" y1="74" x2="95" y2="74" />
      <line x1="0" y1="83" x2="95" y2="83" />
      <line x1="0" y1="89" x2="95" y2="89" />
      <line x1="0" y1="95" x2="95" y2="95" />
      <line x1="0" y1="101" x2="95" y2="101" />
      <line x1="0" y1="107" x2="95" y2="107" />
      <line x1="0" y1="113" x2="95" y2="113" />
      <line x1="0" y1="120" x2="95" y2="120" style="stroke-width:2" />
    
      <!-- Vertical lines -->
      <line x1="0" y1="0" x2="0" y2="120" style="stroke-width:2" />
      <line x1="2" y1="0" x2="2" y2="120" />
      <line x1="8" y1="0" x2="8" y2="120" />
      <line x1="14" y1="0" x2="14" y2="120" />
      <line x1="17" y1="0" x2="17" y2="120" />
      <line x1="23" y1="0" x2="23" y2="120" />
      <line x1="29" y1="0" x2="29" y2="120" />
      <line x1="32" y1="0" x2="32" y2="120" />
      <line x1="38" y1="0" x2="38" y2="120" />
      <line x1="44" y1="0" x2="44" y2="120" />
      <line x1="47" y1="0" x2="47" y2="120" />
      <line x1="53" y1="0" x2="53" y2="120" />
      <line x1="59" y1="0" x2="59" y2="120" />
      <line x1="62" y1="0" x2="62" y2="120" />
      <line x1="68" y1="0" x2="68" y2="120" />
      <line x1="74" y1="0" x2="74" y2="120" />
      <line x1="77" y1="0" x2="77" y2="120" />
      <line x1="83" y1="0" x2="83" y2="120" />
      <line x1="89" y1="0" x2="89" y2="120" />
      <line x1="95" y1="0" x2="95" y2="120" style="stroke-width:2" />
    
      <!-- Colored Rectangle -->
      <polygon points="0.0,0.0 95.30444964871195,0.0 95.30444964871195,120.0 0.0,120.0" style="fill:#8B4903A0;stroke-width:0"/>
    
      <!-- Text -->
      <text x="47.652225" y="140.000000" font-size="1.0rem" font-weight="100" text-anchor="middle" >8139</text>
      <text x="115.304450" y="60.000000" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(-90,115.304450,60.000000)">10248</text>
    </svg>
            </td>
        </tr>
    </table></div></li><li class='xr-var-item'><div class='xr-var-name'><span>local_incidence_angle</span></div><div class='xr-var-dims'>(y, x)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>dask.array&lt;chunksize=(256, 256), meta=np.ndarray&gt;</div><input id='attrs-234751fd-c8d6-4c4c-8622-6cb321a6579a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-234751fd-c8d6-4c4c-8622-6cb321a6579a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8232d764-f787-49c5-ad5d-3761ce351cd9' class='xr-var-data-in' type='checkbox'><label for='data-8232d764-f787-49c5-ad5d-3761ce351cd9' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><table>
        <tr>
            <td>
                <table style="border-collapse: collapse;">
                    <thead>
                        <tr>
                            <td> </td>
                            <th> Array </th>
                            <th> Chunk </th>
                        </tr>
                    </thead>
                    <tbody>
    
                        <tr>
                            <th> Bytes </th>
                            <td> 318.18 MiB </td>
                            <td> 256.00 kiB </td>
                        </tr>
    
                        <tr>
                            <th> Shape </th>
                            <td> (10248, 8139) </td>
                            <td> (256, 256) </td>
                        </tr>
                        <tr>
                            <th> Dask graph </th>
                            <td colspan="2"> 1312 chunks in 2 graph layers </td>
                        </tr>
                        <tr>
                            <th> Data type </th>
                            <td colspan="2"> float32 numpy.ndarray </td>
                        </tr>
                    </tbody>
                </table>
            </td>
            <td>
            <svg width="145" height="170" style="stroke:rgb(0,0,0);stroke-width:1" >
    
      <!-- Horizontal lines -->
      <line x1="0" y1="0" x2="95" y2="0" style="stroke-width:2" />
      <line x1="0" y1="5" x2="95" y2="5" />
      <line x1="0" y1="11" x2="95" y2="11" />
      <line x1="0" y1="17" x2="95" y2="17" />
      <line x1="0" y1="23" x2="95" y2="23" />
      <line x1="0" y1="29" x2="95" y2="29" />
      <line x1="0" y1="35" x2="95" y2="35" />
      <line x1="0" y1="44" x2="95" y2="44" />
      <line x1="0" y1="50" x2="95" y2="50" />
      <line x1="0" y1="56" x2="95" y2="56" />
      <line x1="0" y1="62" x2="95" y2="62" />
      <line x1="0" y1="68" x2="95" y2="68" />
      <line x1="0" y1="74" x2="95" y2="74" />
      <line x1="0" y1="83" x2="95" y2="83" />
      <line x1="0" y1="89" x2="95" y2="89" />
      <line x1="0" y1="95" x2="95" y2="95" />
      <line x1="0" y1="101" x2="95" y2="101" />
      <line x1="0" y1="107" x2="95" y2="107" />
      <line x1="0" y1="113" x2="95" y2="113" />
      <line x1="0" y1="120" x2="95" y2="120" style="stroke-width:2" />
    
      <!-- Vertical lines -->
      <line x1="0" y1="0" x2="0" y2="120" style="stroke-width:2" />
      <line x1="2" y1="0" x2="2" y2="120" />
      <line x1="8" y1="0" x2="8" y2="120" />
      <line x1="14" y1="0" x2="14" y2="120" />
      <line x1="17" y1="0" x2="17" y2="120" />
      <line x1="23" y1="0" x2="23" y2="120" />
      <line x1="29" y1="0" x2="29" y2="120" />
      <line x1="32" y1="0" x2="32" y2="120" />
      <line x1="38" y1="0" x2="38" y2="120" />
      <line x1="44" y1="0" x2="44" y2="120" />
      <line x1="47" y1="0" x2="47" y2="120" />
      <line x1="53" y1="0" x2="53" y2="120" />
      <line x1="59" y1="0" x2="59" y2="120" />
      <line x1="62" y1="0" x2="62" y2="120" />
      <line x1="68" y1="0" x2="68" y2="120" />
      <line x1="74" y1="0" x2="74" y2="120" />
      <line x1="77" y1="0" x2="77" y2="120" />
      <line x1="83" y1="0" x2="83" y2="120" />
      <line x1="89" y1="0" x2="89" y2="120" />
      <line x1="95" y1="0" x2="95" y2="120" style="stroke-width:2" />
    
      <!-- Colored Rectangle -->
      <polygon points="0.0,0.0 95.30444964871195,0.0 95.30444964871195,120.0 0.0,120.0" style="fill:#8B4903A0;stroke-width:0"/>
    
      <!-- Text -->
      <text x="47.652225" y="140.000000" font-size="1.0rem" font-weight="100" text-anchor="middle" >8139</text>
      <text x="115.304450" y="60.000000" font-size="1.0rem" font-weight="100" text-anchor="middle" transform="rotate(-90,115.304450,60.000000)">10248</text>
    </svg>
            </td>
        </tr>
    </table></div></li></ul></div></li><li class='xr-section-item'><input id='section-7106938b-a1e9-4000-a296-05b8f1fa4dd9' class='xr-section-summary-in' type='checkbox'  ><label for='section-7106938b-a1e9-4000-a296-05b8f1fa4dd9' class='xr-section-summary' >Indexes: <span>(2)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-index-name'><div>x</div></div><div class='xr-index-preview'>PandasIndex</div><input type='checkbox' disabled/><label></label><input id='index-a38070e7-1908-489c-bda8-d6981f8eb6a1' class='xr-index-data-in' type='checkbox'/><label for='index-a38070e7-1908-489c-bda8-d6981f8eb6a1' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Index([422525.0, 422535.0, 422545.0, 422555.0, 422565.0, 422575.0, 422585.0,
           422595.0, 422605.0, 422615.0,
           ...
           503815.0, 503825.0, 503835.0, 503845.0, 503855.0, 503865.0, 503875.0,
           503885.0, 503895.0, 503905.0],
          dtype=&#x27;float64&#x27;, name=&#x27;x&#x27;, length=8139))</pre></div></li><li class='xr-var-item'><div class='xr-index-name'><div>y</div></div><div class='xr-index-preview'>PandasIndex</div><input type='checkbox' disabled/><label></label><input id='index-75f17ea6-170b-43e9-9d4f-2956307358b6' class='xr-index-data-in' type='checkbox'/><label for='index-75f17ea6-170b-43e9-9d4f-2956307358b6' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Index([4573845.0, 4573835.0, 4573825.0, 4573815.0, 4573805.0, 4573795.0,
           4573785.0, 4573775.0, 4573765.0, 4573755.0,
           ...
           4471465.0, 4471455.0, 4471445.0, 4471435.0, 4471425.0, 4471415.0,
           4471405.0, 4471395.0, 4471385.0, 4471375.0],
          dtype=&#x27;float64&#x27;, name=&#x27;y&#x27;, length=10248))</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-513be2c3-134a-4cd7-abd5-3a237768cde2' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-513be2c3-134a-4cd7-abd5-3a237768cde2' class='xr-section-summary'  title='Expand/collapse section'>Attributes: <span>(0)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><dl class='xr-attrs'></dl></div></li></ul></div></div>



