# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zenoml_image_segmentation']

package_data = \
{'': ['*'], 'zenoml_image_segmentation': ['frontend/*']}

setup_kwargs = {
    'name': 'zenoml-image-segmentation',
    'version': '0.0.1',
    'description': 'Image Segmentation for Zeno',
    'long_description': '# Zeno View for Image Segmentation\n\n## Development\n\nFirst, build the frontend:\n\n```bash\ncd frontend\nnpm install\nnpm run build\n```\n\n## Install\n\nInstall the package from PyPI:\n\n```\npip install zenoml_image_segmentation\n```\n\nAnd pass as the `task` argument to a Zeno `.toml` file.\n\n### [Follow the documentation to get started](https://dig.cmu.edu/zeno/intro.html)\n',
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
