# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['urdfenvs',
 'urdfenvs.albert_reacher',
 'urdfenvs.albert_reacher.envs',
 'urdfenvs.albert_reacher.resources',
 'urdfenvs.boxer_robot',
 'urdfenvs.boxer_robot.envs',
 'urdfenvs.boxer_robot.resources',
 'urdfenvs.dual_arm',
 'urdfenvs.dual_arm.envs',
 'urdfenvs.dual_arm.resources',
 'urdfenvs.keyboard_input',
 'urdfenvs.mobile_reacher',
 'urdfenvs.mobile_reacher.envs',
 'urdfenvs.mobile_reacher.resources',
 'urdfenvs.n_link_urdf_reacher',
 'urdfenvs.n_link_urdf_reacher.envs',
 'urdfenvs.n_link_urdf_reacher.resources',
 'urdfenvs.panda_reacher',
 'urdfenvs.panda_reacher.envs',
 'urdfenvs.panda_reacher.resources',
 'urdfenvs.point_robot_urdf',
 'urdfenvs.point_robot_urdf.envs',
 'urdfenvs.point_robot_urdf.resources',
 'urdfenvs.prius',
 'urdfenvs.prius.envs',
 'urdfenvs.prius.resources',
 'urdfenvs.sensors',
 'urdfenvs.tiago_reacher',
 'urdfenvs.tiago_reacher.envs',
 'urdfenvs.tiago_reacher.resources',
 'urdfenvs.urdfCommon']

package_data = \
{'': ['*'],
 'urdfenvs.albert_reacher.resources': ['meshes/*',
                                       'meshes/collision/*',
                                       'meshes/visual/*'],
 'urdfenvs.boxer_robot.resources': ['meshes/collision/*', 'meshes/visual/*'],
 'urdfenvs.mobile_reacher.resources': ['meshes/collision/*', 'meshes/visual/*'],
 'urdfenvs.panda_reacher.resources': ['meshes/collision/*', 'meshes/visual/*'],
 'urdfenvs.prius.resources': ['meshes/*'],
 'urdfenvs.tiago_reacher.resources': ['pal_gripper_description/meshes/*',
                                      'pmb2_description/meshes/base/*',
                                      'pmb2_description/meshes/meshes/*',
                                      'pmb2_description/meshes/objects/*',
                                      'pmb2_description/meshes/sensors/*',
                                      'pmb2_description/meshes/wheels/*',
                                      'tiago_description/meshes/arm/*',
                                      'tiago_description/meshes/head/*',
                                      'tiago_description/meshes/sensors/xtion_pro_live/*',
                                      'tiago_description/meshes/torso/*',
                                      'tiago_dual_description/meshes/torso/*'],
 'urdfenvs.urdfCommon': ['meshes/*']}

install_requires = \
['gym>=0.21.0,<0.22.0',
 'numpy>=1.19.0,<2.0.0',
 'pybullet>=3.2.1,<4.0.0',
 'pytest>=6.2.5,<7.0.0',
 'urdfpy>=0.0.22,<0.0.23']

extras_require = \
{'docs': ['Sphinx==4.2.0',
          'sphinx-rtd-theme==1.0.0',
          'sphinxcontrib-napoleon==0.7'],
 'keyboard': ['pynput>=1.7.6,<2.0.0', 'multiprocess>=0.70.12,<0.71.0'],
 'scenes': ['motion-planning-scenes>=0.1.19,<0.2.0']}

setup_kwargs = {
    'name': 'urdfenvs',
    'version': '0.2.2',
    'description': 'Simple simulation environment for robots, based on the urdf files.',
    'long_description': None,
    'author': 'Max Spahn',
    'author_email': 'm.spahn@tudelft.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<3.11',
}


setup(**setup_kwargs)
