# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymetaphone_br']

package_data = \
{'': ['*']}

install_requires = \
['unidecode']

setup_kwargs = {
    'name': 'pymetaphone-br',
    'version': '0.0.1',
    'description': 'Pacote do algoritmo Metaphone para a língua portuguesa ',
    'long_description': None,
    'author': 'Bruno',
    'author_email': 'bruno@escavador.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
