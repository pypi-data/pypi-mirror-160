# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['invertedai_drive']

package_data = \
{'': ['*']}

install_requires = \
['ipympl==0.9.1',
 'ipywidgets==7.7.1',
 'jupyterlab==3.4.4',
 'numpy==1.21.2',
 'opencv-python==4.6.0.66',
 'python-dotenv>=0.20.0,<0.21.0',
 'torch>=1.11.0,<2.0.0']

setup_kwargs = {
    'name': 'invertedai-drive',
    'version': '0.1.0',
    'description': 'Client SDK for InvertedAI Drive',
    'long_description': '# InvertedAI Drive\n',
    'author': 'Inverted AI',
    'author_email': 'info@inverted.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
