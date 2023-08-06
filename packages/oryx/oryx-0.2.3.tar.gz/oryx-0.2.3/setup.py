# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oryx',
 'oryx.bijectors',
 'oryx.core',
 'oryx.core.interpreters',
 'oryx.core.interpreters.inverse',
 'oryx.core.ppl',
 'oryx.core.state',
 'oryx.distributions',
 'oryx.experimental',
 'oryx.experimental.autoconj',
 'oryx.experimental.matching',
 'oryx.experimental.mcmc',
 'oryx.experimental.nn',
 'oryx.experimental.optimizers',
 'oryx.internal',
 'oryx.tools',
 'oryx.util']

package_data = \
{'': ['*'], 'oryx': ['examples/notebooks/*']}

install_requires = \
['jax==0.3.15', 'jaxlib==0.3.15', 'tfp-nightly[jax]==0.17.0.dev20220722']

setup_kwargs = {
    'name': 'oryx',
    'version': '0.2.3',
    'description': 'Probabilistic programming and deep learning in JAX',
    'long_description': None,
    'author': 'Google LLC',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
