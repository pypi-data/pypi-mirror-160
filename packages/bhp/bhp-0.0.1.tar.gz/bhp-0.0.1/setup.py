# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bhp', 'bhp.lib']

package_data = \
{'': ['*']}

install_requires = \
['click', 'rich']

entry_points = \
{'console_scripts': ['bhp = bhp.__main__:cli']}

setup_kwargs = {
    'name': 'bhp',
    'version': '0.0.1',
    'description': '',
    'long_description': '<div align="center">\n\n# bhp\n\nbhp is a BloodHound user file parser!\n\n<br>\n\n[Installation](#installation) •\n[Getting started](#getting-started) •\n[Usage](#usage) •\n[Coming Soon](#coming-soon)\n\n</div><br>\n\n</div>\n<br>\n\n## Installation\n\nbhp supports all major operating systems and can be installed for the PyPi using the following command:\n\n```\npipx install bhp\n```\n\nIf this tool is not yet availible via PyPi, you can install it directly from the repository using:\n\n```\ngit clone https://github.com/puzzlepeaches/bhp.git\ncd bhp && pip3 install .\n```\n\nFor development, clone the repository and install it locally using poetry.\n\n```\ngit clone https://github.com/puzzlepeaches/bhp.git && cd bhp\npoetry shell && poetry install\n```\n\n<br>\n\n## Getting started\n\nbhp supports the latest BloodHound user json file format. Let\'s say you ran a BloodHound export on an enagement last summer and now the client is back and asking for social engineering servies. If you want to cheat and get as much coverage as possible, you can parse your previous BloodHound export for users with mailboxes for phishing.\n\n```\nbhp gophish 20210414091456_users.json acmecorp.gophish.csv\n```\n\nWith the output file, you can go into the Gophish web application and add the users to the campaign super easily.\n\n<br>\n\n## Usage\n\nThe bhp help menu is shown below:\n\n```\nUsage: bhp [OPTIONS] COMMAND [ARGS]...\n\n  Parse BloodHound JSON userfiles for external use.\n\nOptions:\n  -h, --help  Show this message and exit.\n\nCommands:\n  gophish  Outputs a gophish import compatible csv file.\n  stdout   Outputs specified type to stdout.\n  txt      Outputs specified type to a text file.\n```\n\nThe stdout and txt modules allow the user to specify a desired output type. Let\'s say you want to get an idea of the most common title for users in your export. You can do something like:\n\n```\nbhp stdout title 20210414091456_users.json | sort -u\n```\n\n<br>\n\n## Thanks\n\n- The BloodHound team for making me stare a graphs all day\n- The [Gophish](https://gophish.io/) team for making me mod their project to land phishing emails.\n- The Sprocket team member that created the first iteration of this tool way back.\n',
    'author': 'Nicholas Anastasi',
    'author_email': 'nanastasi@sprocketsecurity.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/puzzlepeaches/bhp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
