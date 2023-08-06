# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jfscripts', 'jfscripts.work_in_progress']

package_data = \
{'': ['*']}

install_requires = \
['termcolor>=1.1.0,<2.0.0', 'typing-extensions>=4.3.0,<5.0.0']

entry_points = \
{'console_scripts': ['dns-ipv6-prefix.py = jfscripts.dns_ipv6_prefix:main',
                     'extract-pdftext.py = jfscripts.extract_pdftext:main',
                     'find-dupes-by-size.py = '
                     'jfscripts.find_dupes_by_size:main',
                     'image-into-pdf.py = jfscripts.image_into_pdf:main',
                     'list-files.py = jfscripts.list_files:main',
                     'mac-to-eui64.py = jfscripts.mac_to_eui64:main',
                     'pdf-compress.py = jfscripts.pdf_compress:main']}

setup_kwargs = {
    'name': 'jfscripts',
    'version': '1.1.0',
    'description': 'A collection of my Python scripts. Maybe they are useful for someone else.',
    'long_description': '.. image:: http://img.shields.io/pypi/v/jfscripts.svg\n    :target: https://pypi.org/project/jfscripts\n    :alt: This package on the Python Package Index\n\n.. image:: https://github.com/Josef-Friedrich/jfscripts/actions/workflows/tests.yml/badge.svg\n    :target: https://github.com/Josef-Friedrich/jfscripts/actions/workflows/tests.yml\n    :alt: Tests\n\n.. image:: https://readthedocs.org/projects/jfscripts/badge/?version=latest\n    :target: https://jfscripts.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\njfscripts\n=========\n\nA collection of my Python scripts. They all end with the file extension “py”.\nMaybe they are useful for someone else.\n\ndns-ipv6-prefix.py\n------------------\n\n:: \n\n    usage: dns-ipv6-prefix.py [-h] [-V] dnsname\n\n    Get the ipv6 prefix from a DNS name.\n\n    positional arguments:\n      dnsname        The DNS name, e. g. josef-friedrich.de\n\n    optional arguments:\n      -h, --help     show this help message and exit\n      -V, --version  show program\'s version number and exit\n\nextract-pdftext.py\n------------------\n\n:: \n\n    usage: extract-pdftext.py [-h] [-c] [-v] [-V] file\n\n    positional arguments:\n      file            A PDF file containing text\n\n    optional arguments:\n      -h, --help      show this help message and exit\n      -c, --colorize  Colorize the terminal output.\n      -v, --verbose   Make the command line output more verbose.\n      -V, --version   show program\'s version number and exit\n\nfind-dupes-by-size.py\n---------------------\n\n:: \n\n    usage: find-dupes-by-size.py [-h] [-V] path\n\n    Find duplicate files by size.\n\n    positional arguments:\n      path           A directory to recursively search for duplicate files.\n\n    optional arguments:\n      -h, --help     show this help message and exit\n      -V, --version  show program\'s version number and exit\n\nlist-files.py\n-------------\n\n:: \n\n    usage: list-files.py [-h] [-V] input_files [input_files ...]\n\n    This is a script to demonstrate the list_files() function in this file.\n\n    list-files.py a.txt\n    list-files.py a.txt b.txt c.txt\n    list-files.py (asterisk).txt\n    list-files.py "(asterisk).txt"\n    list-files.py dir/\n    list-files.py "dir/(asterisk).txt"\n\n    positional arguments:\n      input_files    Examples for this arguments are: “a.txt”, “a.txt b.txt\n                     c.txt”, “(asterisk).txt”, “"(asterisk).txt"”, “dir/”,\n                     “"dir/(asterisk).txt"”\n\n    optional arguments:\n      -h, --help     show this help message and exit\n      -V, --version  show program\'s version number and exit\n\nmac-to-eui64.py\n---------------\n\n:: \n\n    usage: mac-to-eui64.py [-h] [-V] mac prefix\n\n    Convert mac addresses to EUI64 ipv6 addresses.\n\n    positional arguments:\n      mac            The mac address.\n      prefix         The ipv6 /64 prefix.\n\n    optional arguments:\n      -h, --help     show this help message and exit\n      -V, --version  show program\'s version number and exit\n\nimage-into-pdf.py\n-----------------\n\n:: \n\n    usage: image-into-pdf.py [-h] [-c] [-v] [-V]\n                             {add,ad,a,convert,cv,c,replace,re,r} ...\n\n    Add or replace one page in a PDF file with an image file of the same page\n    size.\n\n    positional arguments:\n      {add,ad,a,convert,cv,c,replace,re,r}\n                            Subcmd_args\n\n    optional arguments:\n      -h, --help            show this help message and exit\n      -c, --colorize        Colorize the terminal output.\n      -v, --verbose         Make the cmd_args line output more verbose.\n      -V, --version         show program\'s version number and exit\n\n',
    'author': 'Josef Friedrich',
    'author_email': 'josef@friedrich.rocks',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Josef-Friedrich/python-scripts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
