# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xarray_quantity']

package_data = \
{'': ['*']}

install_requires = \
['astropy>5.0.3', 'xarray>2022']

setup_kwargs = {
    'name': 'xarray-quantity',
    'version': '0.1.5',
    'description': 'xarray extension which supports astropy quantities.',
    'long_description': '# xarray-quantity\n\n[![PyPI](https://img.shields.io/pypi/v/xarray-quantity.svg?label=PyPI&style=flat-square)](https://pypi.org/pypi/xarray-quantity/)\n[![Python](https://img.shields.io/pypi/pyversions/xarray-quantity.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/pypi/xarray-quantity/)\n[![Test](https://img.shields.io/github/workflow/status/KaoruNishikawa/xarray-quantity/Test?logo=github&label=Test&style=flat-square)](https://github.com/KaoruNishikawa/xarray-quantity/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\nxarray extension which supports astropy quantities.\n\n## Features\n\nThis library provides:\n\n- xarray DataArray and Dataset with units.\n\n## Installation\n\n```shell\npip install xarray-quantity\n```\n\n## Usage\n\n### QuantityArray\n\nTo create a DataArray with units, use `QuantityArray` class. The arguments are compatible with DataArray, except the keyword argument `unit`.\n\n```python\n>>> qa = QuantityArray([1, 2, 3, 4, 5], unit="km")\n>>> qa.data\n[1, 2, 3, 4, 5] km\n>>> qa.unit\nkm\n```\n\n### QuantitySet\n\nTo create a Dataset with units, use `QuantitySet` class. This class also has compatibility with xarray\'s Dataset.\n\n```python\n>>> arrays = {\n...     "qa1": QuantityArray([1, 2, 3, 4, 5], unit="km/s"),\n...     "qa2": QuantityArray([11, 12, 13, 14, 15]),\n...     "da3": xr.DataArray([111, 112, 113, 114, 115])\n... }\n>>> qs = QuantitySet(arrays)\n>>> qs.qa1.data\n[1, 2, 3, 4, 5] km / s\n>>> qs.qa2\nxarray.QuantityArray \'qa2\' (dim_0: 5)\n<Quantity [11., 12., 13., 14., 15.] km / s>\nCoordinates: (0)\nAttributes: (0)\n```\n\n---\n\nThis library is using [Semantic Versioning](https://semver.org).\n',
    'author': 'KaoruNishikawa',
    'author_email': 'k.nishikawa@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/KaoruNishikawa/xarray-quantity',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
