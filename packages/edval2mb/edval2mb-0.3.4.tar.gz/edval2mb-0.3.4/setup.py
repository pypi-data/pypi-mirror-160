# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edval2mb', 'edval2mb.cli']

package_data = \
{'': ['*']}

install_requires = \
['click-config-file>=0.6.0,<0.7.0',
 'click>=8.1.3,<9.0.0',
 'pandas>=1.4.3,<2.0.0']

entry_points = \
{'console_scripts': ['edval2mb = edval2mb.cli.main:main']}

setup_kwargs = {
    'name': 'edval2mb',
    'version': '0.3.4',
    'description': 'Convert edval export to ManageBac CSV upload for timetables',
    'long_description': '# edval2mb\n\nConvert edval export of schedule to ManageBac CSV. Can be used as csv timetable upload\n\n## Install\n\nPlease install python version 3.9 or above. On Mac, you can use [brew](https://brew.sh), and on Windows, you can use the Microsoft Store.\n\nBest practice with Python is to create virtual environments to install tools. It is recommended. The most straight-forward way to create and use a virtual environment is the follwing:\n\n```\npython3 -m venv venv\n```\n\nThat sets up the virtual environment. Then, to activate the virtual environment:\n\n```\nsource venv/bin/activate  # Mac/Unix\n./venv/Bin/Activate  # Windows\n```\n\nOnce the virtual environment is activated, install:\n\n```\npip install edval2mb\n```\n\nYou will now have the command line tool "edval2mb" available in the terminal.\n\n## To use\n\nThis tool takes as input the csv export, and will save the result into a file that is output when complete.\n\n```\nedval2mb path/to/exported/csv.csv to_mb\n```\n\nOutput:\n\n```\nSaved csv of 1365 rows (including header) and 5 columns to /path/to/managebac_timetable.csv\n```\n\n## Options\n\nTo view the options available on the `to_mb` command, please see the output to this command:\n\n```\nedval2mb path/to/exported/csv.csv \n```\n\nOutput:\n\n```\nOptions:\n  --academic-year TEXT          The value passed here will be output to each\n                                row of the output\n  --day-start-index INTEGER     Some schools ManageBac timetable starts from\n                                day 0.  In this case, you can pass 0 to this\n                                option.\n  --period-start-index INTEGER  Some schools have their timetable start with\n                                0.  In this case, you can pass 0 to this\n                                option.\n  --day TEXT                    If the exported csv uses days of week other\n                                than Mon, Tue, Wed Thu Friday, you can specify\n                                these by passing multiple --day Lundi --day\n                                Marchi etc in sequential order\n  --output-path TEXT            The path (including file name) of the output\n                                file\n  --help                        Show this message and exit.\n```\n\n',
    'author': 'Adam Morris',
    'author_email': 'classroomtechtools.ctt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
