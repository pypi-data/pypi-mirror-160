# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src/crawler'}

packages = \
['crawler', 'crawler.parsers', 'crawler.spiders', 'parsers', 'spiders']

package_data = \
{'': ['*'], 'crawler': ['drivers/*']}

install_requires = \
['black>=22.6.0,<23.0.0',
 'bs4',
 'hyperopt>=0.2.7,<0.3.0',
 'jupyter',
 'matplotlib>=3.4.3,<4.0.0',
 'nltk>=3.6.5,<4.0.0',
 'pandas>=1.3.4,<2.0.0',
 'pymupdf>=1.20.0,<2.0.0',
 'pytest>=7.1.2,<8.0.0',
 'scrapy>=2.6.1,<3.0.0',
 'selenium>=3.141.0,<4.0.0',
 'sklearn',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'digital-literacy',
    'version': '0.1.0',
    'description': 'Level at which course modules of German/Bavarian universities teach about Digitalization',
    'long_description': None,
    'author': 'Sanjay Jayaprakash',
    'author_email': 'sanjay.jayaprakash@tum.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
