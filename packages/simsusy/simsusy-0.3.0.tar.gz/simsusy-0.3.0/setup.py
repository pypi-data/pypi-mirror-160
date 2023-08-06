# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simsusy', 'simsusy.mssm', 'simsusy.tests']

package_data = \
{'': ['*'],
 'simsusy.tests': ['outputs/mssm1.mg5_tree_calculator.v1',
                   'outputs/mssm1.mg5_tree_calculator.v1',
                   'outputs/mssm1.mg5_tree_calculator.v1',
                   'outputs/mssm1.mg5_tree_calculator.v1',
                   'outputs/mssm1.mg5_tree_calculator.v1',
                   'outputs/mssm1.mg5_tree_calculator.v2',
                   'outputs/mssm1.mg5_tree_calculator.v2',
                   'outputs/mssm1.mg5_tree_calculator.v2',
                   'outputs/mssm1.mg5_tree_calculator.v2',
                   'outputs/mssm1.mg5_tree_calculator.v2',
                   'outputs/mssm1.tree_calculator.v1',
                   'outputs/mssm1.tree_calculator.v1',
                   'outputs/mssm1.tree_calculator.v1',
                   'outputs/mssm1.tree_calculator.v1',
                   'outputs/mssm1.tree_calculator.v1',
                   'outputs/mssm1.tree_calculator.v2',
                   'outputs/mssm1.tree_calculator.v2',
                   'outputs/mssm1.tree_calculator.v2',
                   'outputs/mssm1.tree_calculator.v2',
                   'outputs/mssm1.tree_calculator.v2',
                   'outputs/mssm2.tree_calculator.v2',
                   'outputs/mssm2.tree_calculator.v2',
                   'outputs/mssm2.tree_calculator.v2',
                   'outputs/mssm2.tree_calculator.v2',
                   'outputs/mssm2.tree_calculator.v2']}

install_requires = \
['click>=8.1,<9.0',
 'colorama>=0.4.4,<0.5.0',
 'coloredlogs>=15.0,<16.0',
 'numpy>=1.22,<2.0',
 'yaslha>=0.3.3,<0.4.0']

entry_points = \
{'console_scripts': ['simsusy = simsusy.simsusy:simsusy_main']}

setup_kwargs = {
    'name': 'simsusy',
    'version': '0.3.0',
    'description': 'A Python package for simple SUSY spectrum calculation',
    'long_description': '|img_ci|_ |img_cov|_ |img_type|_ |img_license|_ |img_black|_\n\nSimSUSY: simple SUSY spectrum calculators\n=========================================\n\nA framework to call respective "calculators".\n\nA simple example is:\n\n.. code-block:: shell\n\n   simsusy run -c mssm.tree_calculator input.SLHA\n\nwhere ``input.slha`` is a proper input file.\nNote that **calculator is specified by hand**, or should be specified in ``SIMSUSY`` block of the input file.\n\nRemarks / Policies\n------------------\n\n* calculators are stored as ``simsusy/MODEL/NAME_calculator.py`` and called as ``MODEL.NAME_calculator``.\n* ``SIMSUSY`` block in input files must be "eaten" by the calculator and absent in the output file.\n* ``SIMSUSY`` 0–99 are reserved for SimSUSY program.\n* ``SIMSUSY`` 100–999 are for each calculator. However, **these values should not alter physical output** (e.g., "loop order" cannot be specified there!). Instead, prepare another calculator to have different physical output.\n\n\n\nLicense\n-------\n\nThis code set ("software") is licensed to you under |Apache2|_.\nSee ``LICENSE`` file and ``NOTICE`` file for further information.\n\n\n\n\n.. |Apache2| replace:: the Apache License, version 2.0\n.. _Apache2: https://www.apache.org/licenses/LICENSE-2.0\n\n.. _img_ci: https://github.com/misho104/SimSUSY/actions/workflows/unit-test.yaml\n.. |img_ci| image:: https://github.com/misho104/SimSUSY/actions/workflows/unit-test.yaml/badge.svg?branch=master\n  :height: 16px\n\n.. _img_cov: https://codecov.io/gh/misho104/SimSUSY\n.. |img_cov| image:: https://codecov.io/gh/misho104/SimSUSY/branch/master/graph/badge.svg\n  :height: 16px\n\n.. _img_type: https://github.com/misho104/SimSUSY/actions/workflows/type-check.yaml\n.. |img_type| image:: https://github.com/misho104/SimSUSY/actions/workflows/type-check.yaml/badge.svg?branch=master\n  :height: 16px\n\n.. _img_license: https://github.com/misho104/SimSUSY/blob/master/LICENSE\n.. |img_license| image:: https://shields.io/badge/license-Apache--2.0-ff25d1\n  :height: 16px\n  :alt: This package is licensed under the Apache-2.0 License.\n\n.. _img_black: https://github.com/ambv/black\n.. |img_black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n  :height: 16px\n',
    'author': 'Sho Iwamoto (Misho)',
    'author_email': 'webmaster@misho-web.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/misho104/simsusy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
