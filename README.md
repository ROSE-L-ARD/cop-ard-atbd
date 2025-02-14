# rose-l-ard
ROSE-L Analysis Ready Data

Algorithms and utilities for Analysis Ready Data for Copernicus Missions

Enables cloud-native SAR processing via [*Xarray*](https://xarray.pydata.org)
and [*Dask*](https://dask.org).

This Open Source project is sponsored by B-Open - https://www.bopen.eu.

## Install

The easiest way to install *sarsen* is in a *conda* environment.
The following commands create a new environment, activate it, install the package and its dependencies:

```shell
  # cloning from git repository
  git clone https://github.com/bopen/rose-l-ard.git rose-l-ard
  cd rose-l-ard
  # create conda environment
  conda create -n rosel --file env.yaml
  conda activate rosel
  # install rosel package
  pip install -e .
```

## Command line usage


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

## Contributing

The main repository is hosted on GitHub.
Testing, bug reports and contributions are highly welcomed and appreciated:

https://github.com/bopen/sarsen

Lead developer:

- [Federico Minati](https://github.com/effeminati) - [B-Open](https://bopen.eu)

Main contributors:

- [Francesco Vecchioli ](https://github.com/francesco-vecchioli) - [B-Open](https://bopen.eu)
- [Francesco De Zan ](https://github.com/fdz-insar) - [DeltaPhi](https://www.delta-phi.eu/)
- [Juan M Lopez Sanchez ](https://github.com/juanma-lopez) - [University of Alicante](https://www.ua.es/en/)
- [Paco Lopez Dekker ](https://github.com/) - [TU-Delft](https://www.tudelft.nl/en/)

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
