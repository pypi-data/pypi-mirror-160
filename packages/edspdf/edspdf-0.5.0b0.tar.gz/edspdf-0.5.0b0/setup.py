# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edspdf',
 'edspdf.aggregators',
 'edspdf.classifiers',
 'edspdf.extractors',
 'edspdf.extractors.style',
 'edspdf.misc',
 'edspdf.readers',
 'edspdf.transforms',
 'edspdf.visualization']

package_data = \
{'': ['*']}

install_requires = \
['catalogue>=2.0.7,<3.0.0',
 'loguru>=0.6.0,<0.7.0',
 'networkx>=2.6,<3.0',
 'pandas>=1.2,<2.0',
 'pdf2image>=1.16.0,<2.0.0',
 'pdfminer.six>=20220319,<20220320',
 'pydantic>=1.2,<2.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'scipy>=1.7.0,<2.0.0',
 'thinc>=8.0.15,<9.0.0']

setup_kwargs = {
    'name': 'edspdf',
    'version': '0.5.0b0',
    'description': 'Smart text extraction from PDF documents',
    'long_description': '# EDS-PDF\n\nEDS-PDF provides modular framework to extract text from PDF documents.\n\nYou can use it out-of-the-box, or extend it to fit your use-case.\n\n## Getting started\n\nInstall the library with pip:\n\n<div class="termy">\n\n```console\n$ pip install edspdf\n```\n\n</div>\n\nVisit the [documentation](https://datasciencetools-pages.eds.aphp.fr/edspdf/) for more information!\n\n## Acknowledgement\n\nWe would like to thank [Assistance Publique – Hôpitaux de Paris](https://www.aphp.fr/)\nand [AP-HP Foundation](https://fondationrechercheaphp.fr/) for funding this project.\n',
    'author': 'Basile Dura',
    'author_email': 'basile.dura-ext@aphp.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://datasciencetools-pages.eds.aphp.fr/edspdf/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
