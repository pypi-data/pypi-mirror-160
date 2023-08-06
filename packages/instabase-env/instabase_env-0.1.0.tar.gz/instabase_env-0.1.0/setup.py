# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['instabase_env']

package_data = \
{'': ['*']}

install_requires = \
['Pillow==8.1.2',
 'PyPDF2==1.26.0',
 'XlsxWriter==1.0.2',
 'beautifulsoup4==4.6.3',
 'dateparser==0.7.0',
 'nltk==3.4.5',
 'numpy==1.16.5',
 'opencv-contrib-python==3.4.2.17',
 'pandas==1.1.0',
 'pdfkit==0.6.1',
 'regex==2018.01.10',
 'requests==2.22.0',
 'scikit-image==0.16.2',
 'scikit-learn==0.21.3',
 'scipy==1.3.1',
 'spacy==2.3.2',
 'xlwt==1.3.0']

setup_kwargs = {
    'name': 'instabase-env',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Arjoonn Sharma',
    'author_email': 'arjoonn.sharma@instabase.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
