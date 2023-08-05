# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['standup_shows']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4', 'fire', 'requests']

entry_points = \
{'console_scripts': ['standup = standup_shows.standup:main']}

setup_kwargs = {
    'name': 'standup-shows',
    'version': '1.0.1',
    'description': 'Find stand-up comedy shows near you from the command line.',
    'long_description': '<!-- # CLI -->\n# Installation\n```shell\n$ pip install standup-shows\n````\n\n# Basic Usage\n"Search for shows in a 50-mile radius from zipcode 75201 for comics listed in ./comics.txt"\n\n```\n$ standup 75201 50 comics.txt\nMs. Pat:\n    Arlington Improv - Thursday, December 01 at 08:00 PM - https://www.dead-frog.com/live-comedy/event/881867\n    Arlington Improv - Friday, December 02 at 07:30 PM - https://www.dead-frog.com/live-comedy/event/881868\n    Arlington Improv - Friday, December 02 at 09:45 PM - https://www.dead-frog.com/live-comedy/event/881869\n    Arlington Improv - Saturday, December 03 at 07:00 PM - https://www.dead-frog.com/live-comedy/event/881870\n    Arlington Improv - Saturday, December 03 at 09:30 PM - https://www.dead-frog.com/live-comedy/event/881871\n    Arlington Improv - Sunday, December 04 at 07:00 PM - https://www.dead-frog.com/live-comedy/event/881872\n\nMark Normand:\n    Dallas Comedy Club - Wednesday, July 13 at 10:00 PM - https://www.dead-frog.com/live-comedy/event/123455\n    Dallas Comedy Club - Wednesday, July 13 at 11:00 PM - https://www.dead-frog.com/live-comedy/event/123456\n```\n\nThe script takes a few seconds to execute because it scrapes events from the web. You can specify the number of threads to create with the `--max_threads` flag.\n\n```\n$ standup --help\nNAME\n    standup.py - Find stand-up comedy shows that your favorite comedians are scheduled to perform near you.\n\nSYNOPSIS\n    standup.py COMEDIANS ZIPCODE <flags>\n\nDESCRIPTION\n    Find stand-up comedy shows that your favorite comedians are scheduled to perform near you.\n\nPOSITIONAL ARGUMENTS\n    COMEDIANS\n        Type: str\n        A filepath containing a newline-delimited list of comedians in the form of <firstname lastname>.\n    ZIPCODE\n        Type: int\n        The zipcode to search near.\n\nFLAGS\n    --radius=RADIUS\n        Type: int\n        Default: 25\n        The radius in miles around the zipcode to search.\n    --max_threads=MAX_THREADS\n        Type: int\n        Default: 100\n        The maximum number of threads to create. A new thread is created for each URL to scrape.\n\nNOTES\n    You can also use flags syntax for POSITIONAL ARGUMENTS\n```\n\n# Further Development\n- Output to email\n- Find a dataset to add support for musical artists\n',
    'author': 'Cal Warhurst',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/calwarhurst/standup-shows',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
