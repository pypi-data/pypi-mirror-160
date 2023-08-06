# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discord_interactions_flask']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.1.3,<3.0.0',
 'PyNaCl>=1.5.0,<2.0.0',
 'jsons>=1.6.3,<2.0.0',
 'urllib3>=1.26.10,<2.0.0']

setup_kwargs = {
    'name': 'discord-interactions-flask',
    'version': '0.1.1',
    'description': '',
    'long_description': '# discord-interactions-flask\n\nA [Flask](https://github.com/pallets/flask/) extension to support interacting with [Discord Interactions](https://discord.com/developers/docs/interactions/application-commands).\n\nCheck out the [quickstart](https://docs.davidbuckley.ca/discord-interactions-flask/usage/quickstart.html) or the [examples directory](/examples) for an idea of how to use it.\n\n```python\nimport os\n\nfrom flask import Flask\n\nfrom discord_interactions_flask import Discord\nfrom discord_interactions_flask import helpers\nfrom discord_interactions_flask.interactions ChatInteraction\n\napp = Flask(__name__)\napp.config[\'DISCORD_PUBLIC_KEY\'] = os.environ[\'DISCORD_PUBLIC_KEY\']\napp.config[\'DISCORD_CLIENT_ID\'] = os.environ[\'DISCORD_CLIENT_ID\']\napp.config[\'DISCORD_CLIENT_SECRET\'] = os.environ[\'DISCORD_CLIENT_SECRET\']\n\ndiscord = Discord()\n\n@discord.command("slash-example")\ndef chat_command(interaction: ChatInteraction) -> types.InteractionResponse:\n    return helpers.content_response("Hello, World!")\n\nchat_command.description = "Say hello via a slash command"\n\ndiscord.init_app(app)\n```\n',
    'author': 'David Buckley',
    'author_email': 'david@davidbuckley.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/buckley-w-david/discord-interactions-flask',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
