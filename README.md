<!--
  Copyright 2026 European Union

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->

# COP ARD ATBD

> **Repository status:** This repository is archived and read-only. Development is complete and no new updates will be made.

The `cop-ard-atbd` repository hosts deliverables and prototype algorithms developed for the Copernicus Analysis Ready Data (ARD) project.

## Project Structure

The repository separates the documentation sources, the reference package, and the prototyping notebooks:

- `docs/atbd_book/`: Contains the Algorithm Theoretical Baseline Document (ATBD) for the **Coregistered Single-Look Complex (CSLC)** and **Geocoded Multi-Look Phase (GMLP)** products.
- `rosel/`: Contains the Phase 1 reference Python package.
- `notebooks/`: Contains the Phase 1 workflows, analysis notebooks, and tests.

## Installation

Use Conda to create the environment and install the package.

### Prerequisites

- Conda installed on your system.
- Git client configured.

### Setup Steps

1. Clone the repository:

```bash
git clone https://github.com/ROSE-L-ARD/cop-ard-atbd.git
cd cop-ard-atbd
```

2. Create the environment from `env.yaml`:

```bash
conda env create -n rosel -f env.yaml
```

3. Activate the environment:

```bash
conda activate rosel
```

4. Install the package in editable mode:

```bash
pip install -e .
```

## Contributors

**Lead developer:**
* **Federico Minati** ([@effeminati](https://github.com/effeminati)) — [B-Open](https://bopen.eu)

**Contributors:**
* **Alessio Morea** ([@AlessioMorea](https://github.com/AlessioMorea)) — [B-Open](https://bopen.eu)
* **Carmine Frascella** ([@CarmineFrascella](https://github.com/CarmineFrascella)) — [B-Open](https://bopen.eu)
* **Francesco Vecchioli** ([@francesco-vecchioli](https://github.com/francesco-vecchioli)) — [B-Open](https://bopen.eu)
* **Francesco DeZan** ([@fdz-insar](https://github.com/fdz-insar)) — [DeltaPhi](https://www.delta-phi.eu/)
* **Juan M. Lopez-Sanchez** ([@juanma-lopez](https://github.com/juanma-lopez)) — [University of Alicante](https://www.ua.es/en/)
* **Paco López-Dekker** ([@pakodekker](https://github.com/pakodekker)) — [TU Delft](https://www.tudelft.nl/en/)
