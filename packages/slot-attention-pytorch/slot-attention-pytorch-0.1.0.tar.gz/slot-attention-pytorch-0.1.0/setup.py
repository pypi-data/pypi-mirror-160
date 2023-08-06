# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slot_attention_pytorch', 'slot_attention_pytorch.shared']

package_data = \
{'': ['*'], 'slot_attention_pytorch': ['config/*']}

install_requires = \
['hydra-core>=1.2.0,<2.0.0', 'path>=16.4.0,<17.0.0', 'torch>=1.12.0,<2.0.0']

setup_kwargs = {
    'name': 'slot-attention-pytorch',
    'version': '0.1.0',
    'description': 'Pytorch slot-attention implementation of Slot Attention',
    'long_description': None,
    'author': 'mikedev',
    'author_email': 'mik3dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
