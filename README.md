# rose-l-ard
ROSE-L Analysis Ready Data

Algorithms and utilities for Analysis Ready Data for Copernicus Missions

Enables cloud-native SAR processing via [*Xarray*](https://xarray.pydata.org)
and [*Dask*](https://dask.org).

This Open Source project is sponsored by B-Open - https://www.bopen.eu.

## Features and limitations

*Rose-l-ard* is a Python library and command line tool with the following functionalities:

-
-
-

Overall, the software is in the **beta** phase and the usual caveats apply.

Current limitations:

- documentation needs improvement

Non-objectives / Caveat emptor items:

- 

## SAR terrain-correction


## Install

The easiest way to install *rosel* is in a *conda* environment.
The following commands create a new environment, activate it, install the package and its dependencies:

```shell
# cloning from git repository
git clone https://github.com/bopen/rose-l-ard.git rose-l-ard
cd rose-l-ard

# create a new conda environment
conda env create -n rosel -f env.yaml

# activate conda environment
conda activate rosel

# install rosel package
pip install -e .
```

## Test installation
In order to test the correct installation of *rosel* package execute the following command:
```python
# import rosel geocoding module
import rosel.shiroma

  
# check rosel geocoding interface based on area projected algorithm
rosel.shiroma.map_geo_ap?
  
```

## Command line usage

The following command performs a geometric terrain correction:

```shell
  xxxx
```

Performing geometric and radiometric terrain correction is more demanding,
but it is possible to produce the RTC of a full GRD product at a 10m resolution
in one go (and it takes approx 25 minutes on a 32Gb MacBook Pro):

```shell
  xxxx
```

## Python API usage

The python API has entry points to the same commands and it also gives access to several lower level
algorithms, but internal APIs should not be considered stable:

```python
>>> import rosel.io
>>> import rosel.shiroma
>>> cslc = rosel.io.read(product_path)

```


## Reference documentation

This is the list of the reference documents:

- 
-

## Project resources

[![on-push](https://github.com/bopen/sarsen/actions/workflows/on-push.yml/badge.svg)](https://github.com/bopen/sarsen/actions/workflows/on-push.yml)
[![codecov](https://codecov.io/gh/bopen/sarsen/branch/main/graph/badge.svg?token=62S9EXDF0V)](https://codecov.io/gh/bopen/sarsen)

## Contributing

The main repository is hosted on GitHub.
Testing, bug reports and contributions are highly welcomed and appreciated:

https://github.com/bopen/sarsen

Lead developer:

- [Federico Minati](https://github.com/effeminati) - [B-Open](https://bopen.eu)

Main contributors:

- [Francesco Vecchioli ](https://github.com/) - [B-Open](https://bopen.eu)
- [Francesco De Zan ](https://github.com/) - [DeltaPhi](https://)
- [xxxx ](https://github.com/) - [xxxx](https://xxxx)
- [xxxx ](https://github.com/) - [xxxx](https://xxxx)
- [xxxx ](https://github.com/) - [xxxx](https://xxxx)
- [xxxx ](https://github.com/) - [xxxx](https://xxxx)
- [xxxx ](https://github.com/) - [xxxx](https://xxxx)
- [xxxx ](https://github.com/) - [xxxx](https://xxxx)

See also the list of [contributors](https://github.com/bopen/rose-l-ard/contributors) who participated in this project.

## Sponsoring

[B-Open](https://bopen.eu) commits to maintain the project long term and we are happy to accept sponsorships to develop new features.

## License

```
Copyright 2016-2022 B-Open Solutions srl

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```