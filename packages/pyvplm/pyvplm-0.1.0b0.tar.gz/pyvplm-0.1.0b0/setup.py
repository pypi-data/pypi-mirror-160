# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyvplm', 'pyvplm.addon', 'pyvplm.core']

package_data = \
{'': ['*']}

install_requires = \
['ipython',
 'ipywidgets',
 'latex',
 'matplotlib',
 'numpy>=1.22.0',
 'openpyxl',
 'pandas',
 'pint',
 'pydoe2==1.3.0',
 'scikit-learn',
 'scipy',
 'sympy',
 'xlrd',
 'xlwt']

setup_kwargs = {
    'name': 'pyvplm',
    'version': '0.1.0b0',
    'description': 'Variable Power-Law regression Models tool',
    'long_description': '![](logo.png) \n\n![Tests](https://github.com/SizingLab/pyvplm/workflows/Tests/badge.svg)\n[![Documentation Status](https://readthedocs.org/projects/pyvplm/badge/?version=latest)](https://pyvplm.readthedocs.io/en/latest/?badge=latest)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n## About\n\npyVPLM is a package that is developed to help scientist, engineer, etc., to construct power-law and/or polynomial \nregression models on different type of data such as finite-element simulation results, manufacturer data-sheets...\n\nIt integrates various functionalities such as :\n\n- Model parameters reduction based on Buckingham Theorem dimensional analysis and \n- [Pint](https://pint.readthedocs.io/en/0.9/) package with derived functions.\n- Sensitivity and dependency analysis on dimensionless parameter and limited experiments to simplify further model \nexpressions.\n- Construction of optimized experimental design on feasible-physical variables leading to full-factorial design within \ndimensionless space. Those DOE are the inputs of parametrized finite-element models.\n- Regression models construction with increasing  complexity (terms sorted based on their impact) and validation based \non relative error repartition analysis.\n\n## Capabilities\n\n#### Dimensional analysis\n\nThe dimensional analysis has to be conducted on a defined set of physical parameters. It can be performed using \nalternatively `buckingham_theorem` which will return the default solution or `automatic_buckingham` which will propose \ndifferent alternate sets.\n\nBased on the obtained solutions, advanced user can also define manually a new solution set with `force_buckingham` \nfunction.\n\n```\nfrom pyvplm.core.definition import PositiveParameter, PositiveParameterSet\nfrom pyvplm.addon.variablepowerlaw import buckingham_theorem\nd = PositiveParameter(\'d\', [10e-3, 150e-3],\'m\', \'pipe internal diameter\')\ne = PositiveParameter(\'e\', [.1e-3, 10e-3], \'m\', \'pipe thickness\')\nparameter_set = PositiveParameterSet(d,e)\npi_set, _ = buckingham_theorem(parameter_set, track=False)\n```\n\n#### Sensitivity & dependency analysis\n\nOnce dimensional analysis is done, there may be still a huge number of dimensionless parameter to describe a \nperformance criteria (mostly form factor) and DOE construction phase may lead to big experiments number and long \nsimulation times.\n\nThis is to answer this problematic that `pi_sensitivity` and `pi_dependency` functions have been designed. The obtained \ngraph for analysis are based on primary vs. secondary parameters analysis that can be easily adapted using \nconfiguration parameters:\n\n![](./docs/source/_static/Pictures/variablepowerlaw_pi_sensitivity.png)\n\n------\n\n![](./docs/source/_static/Pictures/variablepowerlaw_pi_dependency.png)\n\n#### Optimized design of experiments\n\nThe non-constrained nor reduced experimental set are defined using [pyDOE2](https://github.com/clicumu/pyDOE2) package. \nIt integrates automatic sizing of physical/dimensionless initial test plans and functions for selection based on \ndistance criteria (dimensionless mapping) and spread quality (physical mapping).\n\n![](./docs/source/_static/Pictures/pixdoe_create_const_doe1.png)\n\n------\n\n![](./docs/source/_static/Pictures/pixdoe_create_const_doe2.png)\n\n#### Regression models construction\n\nThe `regression_models` function interpolate results to fit a given order polynomial model within linear or logarithmic \nspace. \n\nWithin log space, the model obtained can be transformed into variable power-law model, indeed:\n\n$$\n\\begin{align}\n    log(\\pi_0) = a_0+a_1 \\cdot log(\\pi_1) + a_{11} \\cdot log(\\pi_1)^2+a_{12} \\cdot log(\\pi_1) \\cdot log(\\pi_2) + a_2 \\cdot log(\\pi_2) +...\n\\end{align}\n$$\n\nCan be expressed in the following form:\n\n$$\n\\begin{align}\n    \\pi_0 = 10^{a_0} \\cdot \\pi_1 ^{a_1 + a_{11} \\cdot log(\\pi_1)+a_{12} \\cdot log(\\pi_2)+...} \\cdot  \\pi_2^{a_2+...} \\cdot ...\n\\end{align}\n$$\n\nThis is the origin of package name since variable power-law model is one of the current research subject of MS2M team \nin [ICA](http://institut-clement-ader.org/home/) Laboratory (Toulouse-France). \n\nRegression coefficients are sorted with increasing magnitude while considering standardized values regression (first \norder terms are selected at the beginning to avoid singularity issues):\n\n![](./docs/source/_static/Pictures/variablepowerlaw_regression_models1.png)\n\n<u>The four criteria to evaluate model fidelity with leave-one-out cross-validation are:</u>\n\n1. Maximal relative error magnitude\n2. Average value of the magnitude of relative error which is a good indicator of both average and standard deviation\n3. Average value of the relative error\n4. Standard deviation of the relative error\n\nOn this example with 2 dimensionless parameters and order 3 polynomial expression, a 5-terms model seems to have good \nrepresentation capabilities.\n\n------\n\nOnce regression models have been constructed, each one of them can be analyzed through the analysis of their relative \nerror using `perform_regression` function:\n\n![](./docs/source/_static/Pictures/variablepowerlaw_perform_regression1.png)\n\n## Examples and notes\n\nFour Jupyter Notebooks have been developed to present tool capabilities and functions. They can be launched \nusing Jupyter Notebook application and opening `.ipynb` files from `master/notebooks` folder.\n\nAdditional documentation on sub-packages (`pyvplm.core`, `pyvplm.addon`) and functions can be found on the online \n[readthedocs](https://pyvplm.readthedocs.io/en/latest/) documentation.\n\n## Install\n\nTo install pyVPLM, simply run:\n\n`pip install pyvplm`\n\n\n## Credit\n\npyVPLM is an adaptation of the work performed by MS2M team at [ICA Laboratory](http://institut-clement-ader.org/) - \nFrance and covers the work done during different doctorate thesis:\n\n- Copyright (C) 2014 - 2017 - [Florian Sanchez](https://www.linkedin.com/in/florian-sanchez-7b65ba43/)\n- Copyright (C) 2017 - 2019 - \n[Francesco De Giorgi](https://www.linkedin.com/in/francesco-de-giorgi/?originalSubdomain=fr)\n\n## Author\n\n[A. Reysset](https://www.researchgate.net/profile/Aurelien-Reysset-2)\n\n## References\n\n- F. Sanchez, M. Budinger, I. Hazyuk, "*Dimensional analysis and surrogate models for thermal modeling of power \n- electronic components*", Electrimacs conference (2017), Toulouse\n- F. Sanchez, M. Budinger, I. Hazyuk, "*Dimensional analysis and surrogate models for the thermal modeling of \nMulti-physics systems*", \n[Applied Thermal Engineering](https://www.researchgate.net/journal/1359-4311_Applied_Thermal_Engineering) \n110 (August 2016)\n\n',
    'author': 'Aurélien REYSSET',
    'author_email': 'aurelien.reysset@insa-toulouse.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SizingLab/pyvplm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
