# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mealieapi']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'python-slugify>=6.1.2,<7.0.0']

setup_kwargs = {
    'name': 'mealieapi',
    'version': '0.0.1rc0',
    'description': 'Control your Mealie instance with python!',
    'long_description': '![mealie-image](https://hay-kot.github.io/mealie/assets/img/home_screenshot.png)\n\n# Mealie API\nIf you are running a self-hosted [Mealie](https://hay-kot.github.io/mealie/) server you can use this library to authenticate yourself with and intereact with it!\nCreate mealplans, import recipes, remove users, modify user groups, upload recipe images.\nAll with MealieAPI.\n\n## Installation\n\n\n## Usage\n\n\n### Authentication\nTo start you need your Mealie server url, and your login credentials or an API key (which you can create at `https://[YOUR_MEALIE_SERVER]/admin/profile`).\nMealieAPI uses the `async`/`await` syntax so you must run it inside an async function or event loop like so (if you are not familiar with async applications already.)\n\n\n```py\nimport asyncio\nfrom mealieapi import MealieClient\n\n\nclient = MealieClient("<YOUR_MEALIE_SERVER_ADDRESS>")\n```\nThis next part depends on whether you have an API key, or your login credentials.\n\nIf you want to use your username and password you must use `await client.login("<USERNAME_OR_EMAIL>", "<PASSWORD>")` or if you are using an API key you need to use `client.authorize("<API_KEY>")` (Note: without the await).\n\n```\nasync def main():\n    await client.login("<USERNAME_OR_EMAIL>", "<PASSWORD>")\n    # OR\n    client.authorize("<API_KEY>")\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(main())\n```\n\n\n',
    'author': 'GrandMoff100',
    'author_email': 'nlarsen23.student@gmail.com',
    'maintainer': 'GrandMoff100',
    'maintainer_email': 'nlarsen23.student@gmail.com',
    'url': 'https://github.com/GrandMoff100/MealieAPI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
