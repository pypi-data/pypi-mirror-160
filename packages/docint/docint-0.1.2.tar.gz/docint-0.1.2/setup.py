# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docint', 'docint.models.layoutlm', 'docint.pipeline', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'google-cloud-storage>=1.44.0,<2.0.0',
 'google-cloud-vision>=2.6.3,<3.0.0',
 'jsview>=1.2,<2.0',
 'more-itertools>=8.12.0,<9.0.0',
 'msgpack>=1.0.3,<2.0.0',
 'numpy<1.22.0',
 'opencv-python>=4.4.0.46,<5.0.0.0',
 'pdf2image>=1.16.0,<2.0.0',
 'pdfplumber>=0.6.0,<0.7.0',
 'polyleven>=0.7,<0.8',
 'pydantic==1.9.0',
 'pyenchant>=3.2.2,<4.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'rich>=12.5.1,<13.0.0',
 'transformers[torch]>=4.20.1,<5.0.0']

extras_require = \
{':extra == "doc"': ['mkdocstrings[python]>=0.19.0,<0.20.0'],
 'dev': ['tox>=3.25.1,<4.0.0',
         'bump2version>=1.0.1,<2.0.0',
         'twine>=4.0.1,<5.0.0',
         'pip>=22.1.2,<23.0.0'],
 'doc': ['mkdocs>=1.3.0,<2.0.0',
         'mkdocs-include-markdown-plugin>=3.5.2,<4.0.0',
         'mkdocs-material>=8.3.9,<9.0.0',
         'mkdocs-autorefs>=0.4.1,<0.5.0'],
 'test': ['flake8>=3.9.2,<4.0.0',
          'black>=22.6.0,<23.0.0',
          'isort>=5.10.1,<6.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest>=7.1.2,<8.0.0',
          'pytest-cov>=3.0.0,<4.0.0']}

setup_kwargs = {
    'name': 'docint',
    'version': '0.1.2',
    'description': 'Extracting information from DOCuments INTelligently.',
    'long_description': '# docInt README\nReadme about docInt, document intelligence\n',
    'author': 'Mukund Deshpande',
    'author_email': 'mukundesh@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mukundesh/docint',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
