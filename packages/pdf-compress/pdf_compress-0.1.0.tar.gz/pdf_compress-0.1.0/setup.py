# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdf_compress']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=2.6.0,<3.0.0', 'jfscripts>=0.5.1,<0.6.0']

entry_points = \
{'console_scripts': ['pdf-compress.py = pdf_compress:main']}

setup_kwargs = {
    'name': 'pdf-compress',
    'version': '0.1.0',
    'description': ' Convert and compress PDF scans. Make scans suitable for imslp.org (International Music Score Library Project). See also https://imslp.org/wiki/IMSLP:Scanning_music_scores. The output files are monochrome bitmap images at a resolution of 600 dpi and the compression format CCITT group 4. .',
    'long_description': ".. image:: http://img.shields.io/pypi/v/pdf-compress.svg\n    :target: https://pypi.org/project/pdf-compress\n    :alt: This package on the Python Package Index\n\n.. image:: https://github.com/Josef-Friedrich/pdf_compress/actions/workflows/tests.yml/badge.svg\n    :target: https://github.com/Josef-Friedrich/pdf_compress/actions/workflows/tests.yml\n    :alt: Tests\n\npdf_compress\n============\n\nConvert and compress PDF scans. Make scans suitable for imslp.org\n(International Music Score Library Project). See also\nhttps://imslp.org/wiki/IMSLP:Scanning_music_scores. The output files are\nmonochrome bitmap images at a resolution of 600 dpi and the compression\nformat CCITT group 4.\n\n:: \n\n    usage: pdf-compress.py [-h] [-c] [-m] [-N] [-v] [-V]\n                           {convert,con,c,extract,ex,e,join,jn,j,samples,sp,s,unify,un,u}\n                           ...\n\n    Convert and compress PDF scans. Make scans suitable for imslp.org\n    (International Music Score Library Project). See also\n    https://imslp.org/wiki/IMSLP:Scanning_music_scores The output files are\n    monochrome bitmap images at a resolution of 600 dpi and the compression format\n    CCITT group 4.\n\n    positional arguments:\n      {convert,con,c,extract,ex,e,join,jn,j,samples,sp,s,unify,un,u}\n                            Subcommand\n\n    options:\n      -h, --help            show this help message and exit\n      -c, --colorize        Colorize the terminal output.\n      -m, --multiprocessing\n                            Use multiprocessing to run commands in parallel.\n      -N, --no-cleanup      Don’t clean up the temporary files.\n      -v, --verbose         Make the command line output more verbose.\n      -V, --version         show program's version number and exit\n\n",
    'author': 'Josef Friedrich',
    'author_email': 'josef@friedrich.rocks',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Josef-Friedrich/pdf_compress',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
