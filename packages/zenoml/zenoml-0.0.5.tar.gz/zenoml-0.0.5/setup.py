# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zeno',
 'zeno.pipeline',
 'zeno.pipeline.filter',
 'zeno.pipeline.lableler',
 'zeno.pipeline.projection']

package_data = \
{'': ['*'],
 'zeno': ['frontend/*', 'frontend/build/*', 'frontend/build/assets/*']}

install_requires = \
['fastapi>=0.75,<0.80',
 'pandas>=1.4.0,<2.0.0',
 'pyarrow>=7.0.0,<8.0.0',
 'tensorflow>=2.9.0,<3.0.0',
 'tomli>=2.0.1,<3.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'umap-learn>=0.5.3,<0.6.0',
 'uvicorn>=0.17.5,<0.19.0',
 'websockets>=10.2,<11.0']

entry_points = \
{'console_scripts': ['zeno = zeno.runner:main']}

setup_kwargs = {
    'name': 'zenoml',
    'version': '0.0.5',
    'description': 'Behavioral Evaluation Framework for Machine Learning',
    'long_description': '<img src="./zeno.png" width="400px"/>\n\n![Github Actions CI tests](https://github.com/cabreraalex/zeno/actions/workflows/test.yml/badge.svg)\n![Github Actions Docs build](https://github.com/cabreraalex/zeno/actions/workflows/book.yml/badge.svg)\n[![codecov](https://codecov.io/gh/cmudig/zeno/branch/main/graph/badge.svg?token=7x5oegcwfn)](https://codecov.io/gh/cmudig/zeno)\n[![code style black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n## Install\n\nInstall the Zeno package from PyPI:\n\n```\npip install zenoml\n```\n\n### [Follow the documentation to get started](https://dig.cmu.edu/zeno/intro.html)\n\n## Development Quick Start + CIFAR-10 Example\n\nAfter cloning the repository:\n\n- Install [`Poetry`](https://python-poetry.org/docs/master/#installing-with-the-official-installer), [`nodejs`](https://nodejs.org/en/download/) and use [`VSCode`](https://code.visualstudio.com/) as your editor.\n- `poetry config virtualenvs.in-project true`\n- `make install`\n\nYou should now be able to run `poetry run zeno`\n\nTo run the CIFAR-10 example:\n\n- `mkdir data; cd data; git clone https://github.com/YoongiKim/CIFAR-10-images`\n- `poetry run zeno ./examples/cifar/tests/zeno.toml`\n- For debugging, you can use the "Run and Debug" sidebar in VSCode (a play button with a bug icon), and run the `zenocifar` configuration.\n\nTo see live changes to the frontend:\n\n- `cd frontend; npm run dev`\n',
    'author': 'Ángel Alexander Cabrera',
    'author_email': 'alex.cabrera@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://dig.cmu.edu/zeno/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
