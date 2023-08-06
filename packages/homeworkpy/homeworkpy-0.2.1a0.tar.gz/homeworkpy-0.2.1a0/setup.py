# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['homeworkpy']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4==4.11.1',
 'recurring-ical-events==1.0.2b0',
 'requests==2.28.0',
 'rich==12.4.4']

setup_kwargs = {
    'name': 'homeworkpy',
    'version': '0.2.1a0',
    'description': 'An all-in-one pythonic student data representation solution.',
    'long_description': "# homework-py\n\n## NOTICE\n\nOnly one singular school's renweb has been confirmed as being supported in initial requests. (This repo is very experiementaldjnkdjnsd) \n\nHallo!! Homework-py is makeshift wrapper of the SIS-s[^1] I deal with as a student, and the library adds pythonic ways of tracking the general data a student may need to keep track of. \n\n### What can this be used for?\n\n> In my personal opinion, there may be streamlined wrappers for systems like Canvas. The difference between this library and that library is that this library attempts > to simplify it down to a single cause - tracking a students todo-s and to-dones. (grades)\n\n- Bots\n- Personal Dashboards\n- Alert Systems \n\n\n### Why is this existing when this has been solved before?\n\nIt is an educational project that I had passion for, so I chose to begin it despite knowing it could bear little fruit :).\n\n**Aside from being a simple and *pointless-ish* educational project,** the main reasons I started this are found [here](reasons.md).\n\n### Awesome dependencies of this library(!!)\n\n(epicly doesn't have time to list them yet) (epicly puts on shades to express coolness factor)\n\n### TODO\n\n- [x] Basic Support for Moodle Calendar OOP Processing\n\n> From my knowledge of (nothingness...) OOP, the library should be using a very basic form of OOP as of the first release. I am not sure though. `¯\\_(ツ)_/¯`\n\n- [x] Implement seperate data flagging for Renweb's calendar (PT 1)\n- [ ] Implement seperate data flagging for Renweb's calendar (PT 2)\n- [x] Implement Renweb Report Card Data Extraction \n- [ ] Clean up code with formatting and formatting\n- [ ] Setup as a python package\n- [ ] Release! (as a standard version with correct semantic versioning)\n",
    'author': 'Nathan Solis',
    'author_email': '66754842+colderinit@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://colderinit.github.io/homework-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
