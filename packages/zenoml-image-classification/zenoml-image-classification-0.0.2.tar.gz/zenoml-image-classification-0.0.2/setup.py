# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zenoml_image_classification']

package_data = \
{'': ['*'], 'zenoml_image_classification': ['frontend/*']}

setup_kwargs = {
    'name': 'zenoml-image-classification',
    'version': '0.0.2',
    'description': 'Image Classification for Zeno',
    'long_description': '# Zeno View for Image Classification\n\n## Install\n\nInstall the package from PyPI:\n\n```\npip install zenoml_image_classification\n```\n\nAnd pass as the `task` argument to a Zeno `.toml` file.\n\n### [Follow the documentation to get started](https://dig.cmu.edu/zeno/intro.html)\n',
    'author': 'Ángel Alexander Cabrera',
    'author_email': 'alex.cabrera@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://dig.cmu.edu/zeno/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
