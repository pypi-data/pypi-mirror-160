# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['userpic']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

extras_require = \
{'cairo': ['CairoSVG>=2.5.2,<3.0.0']}

setup_kwargs = {
    'name': 'tiny-userpic',
    'version': '0.2.0',
    'description': 'A small Python module for userpics creation',
    'long_description': '# Userpic Generator\n\n[![PyPI version](https://badge.fury.io/py/tiny-userpic.svg)](https://pypi.org/project/tiny-userpic/)\n\n## Getting Started\n\n## Installing\n\ntiny-userpic can be installed using pip:\n\n```bash\npip install tiny-userpic\n```\n\n## Usage\n\nTo test that installation was successful, try:\n\n```bash\npython -m userpic --output img.png\n```\n\ntiny-userpic can be used both from the command line and as a Python library.\n\n```python\nfrom userpic import make_userpic\ndata = make_userpic(\n    cells_count=7,\n    cell_size=32,\n    offset=16,\n    data_format="svg",\n)\nwith open("output.svg", "wb") as file:\n    file.write(data)\n```\n',
    'author': 'Aleksandr Shpak',
    'author_email': 'shpaker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shpaker/tiny-userpic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
