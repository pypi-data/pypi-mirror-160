# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vk_cli']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.12.0,<3.0.0', 'click>=8.1.3,<9.0.0', 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['vk = vk_cli.main:command']}

setup_kwargs = {
    'name': 'vk-cli',
    'version': '0.1.1',
    'description': 'VK call api in console',
    'long_description': '# VK CLI\nCall VK API methods from terminal.\n\n## Installation\n\nInstall with pip\n\n```bash\n  pip install vk-cli\n```\n    \n## Usage\nHelp\n```bash\n> vk -h\nUsage: python -m vk [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  -h, --help  Show this message and exit.\n\nCommands:\n  api      Call the API\n  profile  Proile commands\n  shell    start shell\n```\nCreate new profile\n```bash\nvk profile new --access-token <VK TOKEN>\n```\n\nAPI call\n```bash\nvk api users.get user_id=1\n```\n\n\n\n## Shell\nRun Shell\n```bash\nvk shell\n```\nShel is it interactive python shell, but you can call to api vk\n```python\n>>> response = API.users.get(user_id=1)\n>>> user = user["response"][0]\n>>> print(user["first_name"], user["last_name"], sep=" ")\nПавел Дуров\n```',
    'author': 'sergey',
    'author_email': 'saalaus@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/saalaus/vk-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
