# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['noneprompt', 'noneprompt.cli', 'noneprompt.prompts']

package_data = \
{'': ['*']}

install_requires = \
['prompt-toolkit>=3.0.19,<4.0.0']

entry_points = \
{'console_scripts': ['noneprompt = noneprompt.__main__:main']}

setup_kwargs = {
    'name': 'noneprompt',
    'version': '0.1.4',
    'description': 'Prompt toolkit for console interaction',
    'long_description': '# NonePrompt\n\nPrompt toolkit for console interaction.\n\nTyping is supported.\n\n## Installation\n\n```bash\npip install noneprompt\n```\n\n## Usage\n\n### Input\n\n```python\nfrom noneprompt import InputPrompt\n\nInputPrompt("What is your name?", validator=lambda string: True).prompt()\n```\n\n### Confirm\n\n```python\nfrom noneprompt import ConfirmPrompt\n\nConfirmPrompt("Are you sure?", default_choice=False).prompt()\n```\n\n### List\n\n```python\nfrom noneprompt import ListPrompt, Choice\n\nListPrompt("What is your favorite color?", choices=[Choice("Red"), Choice("Blue")]).prompt()\n```\n\n### Checkbox\n\n```python\nfrom noneprompt import CheckboxPrompt, Choice\n\nCheckboxPrompt("Choose your favorite colors", choices=[Choice("Red"), Choice("Blue")]).prompt()\n```\n\n## Try from command line\n\n```bash\nnoneprompt -h\n```\n',
    'author': 'yanyongyu',
    'author_email': 'yyy@nonebot.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nonebot/noneprompt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
