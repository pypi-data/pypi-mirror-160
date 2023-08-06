# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beancount_import_sparkasse']

package_data = \
{'': ['*']}

install_requires = \
['beancount>=2.3.5,<3.0.0']

setup_kwargs = {
    'name': 'beancount-import-sparkasse',
    'version': '0.0.1a0',
    'description': 'Beancount importer plugin for Sparkasse CSV-CAMT exports',
    'long_description': '# Beancount Importer - Sparkasse\n[![tests_badge](https://github.com/laermannjan/beancount-import-sparkasse/actions/workflows/main.yaml/badge.svg)](https://github.com/laermannjan/beancount-import-sparkasse/actions/) [![image](https://img.shields.io/pypi/v/beancount-import-sparkasse.svg)](https://pypi.python.org/pypi/beancount-import-sparkasse) [![image](https://img.shields.io/pypi/pyversions/beancount-import-sparkasse.svg)](https://pypi.python.org/pypi/beancount-import-sparkasse) [![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![license_badge](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n## Installation\nThe importer is available on [PyPI](https://pypi.org/project/beancount-import-sparkasse)\n``` sh\npip install --user beancount-import-sparkasse\n```\n\n## Configuration\nAdd the importer to your `beancount` import config\n\n``` python\nfrom beancount_import_sparkase import SparkasseCSVCAMTImporter\n\nCONFIG = [\n    SparkasseCSVCAMTImporter(\n        iban="DE01 2345 6789 0123 4567 89",\n        account="Assets:DE:Sparkasse:Giro"\n    )\n]\n\n```\n',
    'author': 'Jan Laermann',
    'author_email': 'laermannjan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/laermannjan/beancount-import-sparkasse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
