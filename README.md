# FauxGeo: generate simple geospatial rasters

FauxGeo is a python library that generates simple OSGeo-supported rasters.  The primary purpose for this library is to help test geoprocessing functions.

![PyPI](https://badge.fury.io/py/fauxgeo.png)
![Build](https://travis-ci.org/wbierbower/fauxgeo.svg?branch=master)

## Features

Available Signal Functions

| Signal Function | RasterFactory Method     |
| :------------- | :------------- |
| uniform      | `.uniform(val)`      |
| ramp | `.ramp(zero_index, slope=1)` |
| saw tooth | `.saw(low, high, period)` |
| triangle | `.triangle(low, high, period)` |
| step | `.step(low, high, period)` |
| random range | `.random(low, high)` |
| random from list | `.random(list)` |
| alternating | `.alternate(val1, val2)` |

## Installation

To install FauxGeo, simply:

```bash
$ pip install fauxgeo
```

## Usage

```python
import numpy as np
from fauxgeo import RasterFactory, Affine

options = {
  'affine': Affine.identity(),
  'epsg': 4326,
  'datatype': np.float32,
  'nodata': -9999,
  'driver': 'GTIFF',
  'shape': (10, 10)
}

factory = RasterFactory(**options)
factory.ramp(0, 10, 5).to_file('path/to/file')
```

## Tests

```bash
$ python setup.py test
```
