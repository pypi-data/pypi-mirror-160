# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['planarenvs',
 'planarenvs.ground_robots',
 'planarenvs.ground_robots.envs',
 'planarenvs.mobile_base',
 'planarenvs.mobile_base.envs',
 'planarenvs.mobile_robot',
 'planarenvs.mobile_robot.envs',
 'planarenvs.n_link_reacher',
 'planarenvs.n_link_reacher.envs',
 'planarenvs.n_link_reacher.resources',
 'planarenvs.planar_common',
 'planarenvs.point_robot',
 'planarenvs.point_robot.envs',
 'planarenvs.scenes',
 'planarenvs.sensors']

package_data = \
{'': ['*']}

install_requires = \
['forwardkinematics>=1.0.3,<2.0.0',
 'gym>=0.21.0,<0.22.0',
 'motion-planning-scenes>=0.1.19,<0.2.0',
 'numpy>=1.5.1,<2.0.0',
 'pyglet>=1.5.21,<2.0.0',
 'pylint>=2.13.3,<3.0.0',
 'scipy>=1.5,<2.0']

setup_kwargs = {
    'name': 'planarenvs',
    'version': '1.0.3',
    'description': 'Lightweight open-ai gym environments for planar kinematic chains.',
    'long_description': None,
    'author': 'Max Spahn',
    'author_email': 'm.spahn@tudelft.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<3.11',
}


setup(**setup_kwargs)
