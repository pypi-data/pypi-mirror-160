# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['verifai',
 'verifai.features',
 'verifai.samplers',
 'verifai.simulators',
 'verifai.simulators.car_simulator',
 'verifai.simulators.car_simulator.examples',
 'verifai.simulators.car_simulator.examples.control_utils',
 'verifai.simulators.car_simulator.examples.lanekeeping_LQR',
 'verifai.simulators.carla',
 'verifai.simulators.carla.agents',
 'verifai.simulators.openai_gym',
 'verifai.simulators.webots',
 'verifai.simulators.xplane',
 'verifai.simulators.xplane.utils',
 'verifai.utils']

package_data = \
{'': ['*'], 'verifai.simulators.car_simulator': ['imgs/*']}

install_requires = \
['dill>=0.3.1,<0.4.0',
 'dotmap>=1.3.13,<2.0.0',
 'easydict>=1.9,<2.0',
 'future>=0.18.2,<0.19.0',
 'joblib>=0.14.1,<0.15.0',
 'kmodes>=0.10.2,<0.11.0',
 'matplotlib>=3.2.1,<4.0.0',
 'metric-temporal-logic>=0.1.5,<0.2.0',
 'networkx>=2.6.3,<3.0.0',
 'numpy>=1.21.5,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'progressbar2>=3.53.1,<4.0.0',
 'pygame>=2.1.0,<3.0.0',
 'scenic>=2.1.0b4,<3.0.0',
 'scikit-learn>=1.0,<2.0',
 'scipy>=1.7.3,<2.0.0',
 'statsmodels>=0.13.2,<0.14.0']

extras_require = \
{'bayesopt': ['GPy>=1.9.9,<2.0.0', 'GPyOpt>=1.2.6,<2.0.0'],
 'dev': ['pytest>=6.2.5',
         'pytest-randomly>=3.2.1',
         'tox>=3.14.0,<4.0.0',
         'sphinx>=4.1.0,<6',
         'sphinx-rtd-theme>=0.5.2,<0.6.0',
         'recommonmark>=0.6.0,<0.7.0'],
 'examples': ['tensorflow>=2.8.0,<3.0.0',
              'gym>=0.22,<0.23',
              'pyglet>=1.5.11,<2.0.0',
              'opencv-python>=4.5.3,<5.0.0',
              'pillow>=9.0.1,<10.0.0'],
 'examples:python_version < "3.10"': ['pyproj>=3.0.0,<4.0.0'],
 'examples:python_version >= "3.10" and python_version < "4.0"': ['pyproj>=3.3.0,<4.0.0'],
 'parallel': ['ray>=1.10.0,<2.0.0'],
 'test': ['pytest>=6.2.5', 'pytest-randomly>=3.2.1']}

setup_kwargs = {
    'name': 'verifai',
    'version': '2.1.0b1',
    'description': 'A toolkit for the formal design and analysis of systems that include artificial intelligence (AI) and machine learning (ML) components.',
    'long_description': '[![Documentation Status](https://readthedocs.org/projects/verifai/badge/?version=latest)](https://verifai.readthedocs.io/en/latest/?badge=latest)\n[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)\n\n\n# VerifAI\n\n**VerifAI** is a software toolkit for the formal design and analysis of \nsystems that include artificial intelligence (AI) and machine learning (ML)\ncomponents.\nVerifAI particularly seeks to address challenges with applying formal methods to perception and ML components, including those based on neural networks, and to model and analyze system behavior in the presence of environment uncertainty.\nThe current version of the toolkit performs intelligent simulation guided by formal models and specifications, enabling a variety of use cases including temporal-logic falsification (bug-finding), model-based systematic fuzz testing, parameter synthesis, counterexample analysis, and data set augmentation. Further details may be found in our [CAV 2019 paper](https://people.eecs.berkeley.edu/~sseshia/pubs/b2hd-verifai-cav19.html).\n\nPlease see the [documentation](https://verifai.readthedocs.io/) for installation instructions, tutorials, publications using VerifAI, and more.\n\nVerifAI was designed and implemented by Tommaso Dreossi, Daniel J. Fremont, Shromona Ghosh, Edward Kim, Hadi Ravanbakhsh, Marcell Vazquez-Chanlatte, and Sanjit A. Seshia. \n\nIf you use VerifAI in your work, please cite our [CAV 2019 paper](https://people.eecs.berkeley.edu/~sseshia/pubs/b2hd-verifai-cav19.html) and this website.\n\nIf you have any problems using VerifAI, please submit an issue to the GitHub repository or contact Daniel Fremont at [dfremont@ucsc.edu](mailto:dfremont@ucsc.edu) or Edward Kim at [ek65@berkeley.edu](mailto:ek65@berkeley.edu).\n\n### Repository Structure\n\n* _docs_: sources for the [documentation](https://verifai.readthedocs.io/);\n\n* _examples_: examples and additional documentation for particular simulators, including CARLA, Webots, X-Plane, and OpenAI Gym;\n\n* _src/verifai_: the source for the `verifai` package proper;\n\n* _tests_: the VerifAI test suite.\n',
    'author': 'Tommaso Dreossi',
    'author_email': None,
    'maintainer': 'Daniel Fremont',
    'maintainer_email': 'dfremont@ucsc.edu',
    'url': 'https://github.com/BerkeleyLearnVerify/VerifAI',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
