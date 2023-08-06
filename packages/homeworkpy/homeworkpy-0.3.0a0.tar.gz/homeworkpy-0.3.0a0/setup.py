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
    'version': '0.3.0a0',
    'description': 'An all-in-one pythonic student data representation solution.',
    'long_description': '# homework-py\n[![Released to PyPi](https://github.com/colderinit/homework-py/actions/workflows/release.yml/badge.svg)](https://github.com/colderinit/homework-py/actions/workflows/release.yml)\n\nAn unofficial wrapper for FACTS SIS Renweb. It utilizes a combination of web scraping and data parsing to objectify student data.\nThere *are* plans to branch out to other services like Canvas, Moodle, and Google Classroom.\n\n## Why is this project a little dead?\n\n<details>\n    <summary>TLDR: It got really difficult to keep up with the changes to the websites. Webscraping for makeshift api is not a sound way of doing this. Or at least I think.... `¯\\_(ツ)_/¯` </summary>\n        While I was working on attempting to reverse engineer another login form for Renweb, I came to the conclusion that it was not worth the effort trying to reverse every single login for each and every school. I don\'t know the actual sitemaps of individual pages for different schools as they may be able to edit the layout. I am also pretty stuck on some problems, but I have none to list because they require a ton of access to real datasets from my school\'s database. I think it was when I saw the global login form, I lost the groove that drove the first ~45 commits. If I find anything out, I may hit back to this repo, but for now, this is just a web scraping wrapper for Renweb. (Posing as a normal wrapper for an api that I don\'t have access to. Renweb closed that off a while ago, and you have to partner with them for heavy business - according to what I read.)\n\nThis repo will capture what I was able to write at an educational standpoint. My knowledge of oop and data comprehension. If you go to the school "HCA" and understand the following abbreviations [HCA, FBC] and know a man with a name that sounds like "*o***Kay** *would*" - then I have good news for you. This project does work with our school\'s sitemap because it is the only one I have the ability to test in.\n\n</details>\n\nI won\'t fully let go of this project as a maintainer, I simply would like to step back, (especially because I have no data to work with) and learn a little bit more about the subject matter and target problem. :) Cheers!\n\n## Getting started\n\n### How to install\n\n\n```sh\npip install -U homeworkpy\n```\n\n\n### Features\n\n- [x] Assignment Due Date Sorting\n- [x] Automatic Syncing and Scraping\n- [x] Import Renweb Report cards\n- [x] Keep track of assignments through iCal files\n- [x] Fetch ics files from url or drive path.\n- [ ] import student-visible gradebook (the actual goodness of the project. Dataset not available untill November 2022. :( )  \n\n#### How to Import\n\n```python\nfrom homeworkpy import homework\n```\n\n#### How to initialize a student\n\n```python\nbob_ross = homework.Student(\n    name="Bob Ross",\n    providers={"https://awesomecalendarwebsite.com/bobross/export.ics": True},\n    email="bobross@painting.com",\n    renweb=True,\n    renweb_link="renweb_link",\n    renweb_credentials={\n        "DistrictCode": "HAR-TX",\n        "username": "bross@woopainting!!.com",\n        "password": "titaniumwhite",\n        "UserType": "PARENTSWEB-STUDENT", # this is difficult to narrow down. This is why this library is not applicable to everyone. The form data input names changed per page. \n        "login": "Log+In",\n    },\n    auto_sync=True\n\n)\n```\n\nIn that snippet, we initialize a Student object with the name Bob Ross, and then tell the homework fetcher the icalendar files. The boolean value accompanying the icalendar paths determines whether or not it is a local file on the machine.\nWe provide an optional email, and give the renweb_link. This link is the url of the root of the SIS server.\nThe credentials are given in dictionary form. This is where the project dies a little bit. This is actually form data, but in a python dict. *For now,* I only have the form data working on one website. Feel free to contribute your own school.\n\n```python\nif ns.synced:\n    ns.sort_assignments()\n    ns.print_assignments()\n```\n\nFinally, if the auto_sync automatically synced with all the provided files and servers, we sort the assignments in chronological order, and print them to the console in a nice table format. The output may look like this:\n\n```shell\nBob Ross\'s assignments                                     \n┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓\n┃ Name                     ┃ Description                            ┃ Due Date      ┃ course    ┃\n┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩\n│ Happy Birthday Merica    │Wahoo this is a great day               │ July 04, 2022 │ No course │\n└──────────────────────────┴────────────────────────────────────────┴───────────────┴───────────┘\n```\n\nI made this for fun to see how I could extract my grades with code.\n\n### Awesome dependencies of this library(!!)\n\nFull list of technical dependencies found [here](https://github.com/colderinit/homework-py/network/dependencies).\n\n- beautifulsoup4 = {version = "4.11.1"}\n- recurring-ical-events = {version = "1.0.2b0"}\n- requests = {version = "2.28.0"}\n- rich = {version = "12.4.4"}\n\n## MIT License\n\n`Copyright (c) 2022 Nathan Solis`\n',
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
