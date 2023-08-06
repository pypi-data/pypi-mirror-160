# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['alianator']
install_requires = \
['titlecase>=2.3,<3.0']

setup_kwargs = {
    'name': 'alianator',
    'version': '3.0.0',
    'description': 'A Discord permission name resolver for Pycord',
    'long_description': '# alianator\n\n<a href="https://pypi.org/project/alianator/"><img src="https://img.shields.io/pypi/pyversions/alianator?logo=python&logoColor=white&style=for-the-badge"></a>\n<a href="https://pypi.org/project/alianator/"><img src="https://img.shields.io/pypi/v/alianator?color=green&logo=pypi&logoColor=white&style=for-the-badge"></a>\n<a href="https://github.com/celsiusnarhwal/alianator/releases"><img src="https://img.shields.io/github/v/release/celsiusnarhwal/alianator?color=orange&label=latest%20release&logo=github&sort=semver&style=for-the-badge"></a>\n<a href="https://github.com/celsiusnarhwal/alianator/blob/master/LICENSE.md"><img src="https://img.shields.io/pypi/l/alianator?color=03cb98&style=for-the-badge"></a>\n\nalianator is a Discord permission name resolver for [Pycord](https://github.com/Pycord-Development/pycord). \nIt takes Discord\'s API permission flags (e.g. `manage_guild`) and resolves them to their user-facing aliases (e.g. `Manage Server`).\n\n## Installation\n\n```bash\n$ pip install alianator\n```\n\n[Pycord](https://github.com/Pycord-Development/pycord) is not included as a dependency of alianator, but nonetheless must \nbe installed for it to work. If alianator is unable to import the `discord` namespace, it will raise an `ImportError`.\n\n## Usage\n\nalianator can resolve aliases from `discord.Permissions` objects, integers, strings, tuples, lists of strings, and lists\nof tuples.\n\n```python\nimport alianator\n\nalianator.resolve(arg, mode=mode)\n```\n\nThe optional `mode` flag can be used to specify which permissions should be resolved. If `mode` is `True`, only granted\npermissions will be resolved; if `mode` is `False`, only denied permissions will be resolved; if `mode` is `None`, all\npermissions will be resolved. If `mode` is not explicitly specified, it will default to `True`.\n\n```python\nimport alianator\nimport discord\n\n# Resolving from a discord.Permissions object\nperms = discord.Permissions.general()\naliases = alianator.resolve(perms)\nprint(aliases)\n# [\'Manage Channels\', \'Manage Server\', \'View Audit Log\', \'Read Messages\', \'View Guild Insights\', \'Manage Roles\', \'Manage Webhooks\', \'Manage Emojis and Stickers\']\n\n\n# Resolving from an integer\nperms = 3072\naliases = alianator.resolve(perms)\nprint(aliases)\n# [\'Read Messages\', \'Send Messages\']\n\n\n# Resolving from a string\nperms = "send_tts_messages"\naliases = alianator.resolve(perms)\nprint(aliases)\n# [\'Send Text-To-Speech Messages\']\n\n\n# Resolving from a tuple\nperms = ("moderate_members", True)\naliases = alianator.resolve(perms)\nprint(aliases)\n# [\'Timeout Members\']\n\n\n# Resolving from a list of strings\nperms = ["manage_guild", "manage_emojis"]\naliases = alianator.resolve(perms)\nprint(aliases)\n# [\'Manage Server\', \'Manage Emojis and Stickers\']\n\n\n# Resolving from a list of tuples\nperms = [("use_slash_commands", True), ("use_voice_activation", True)]\naliases = alianator.resolve(perms)\nprint(aliases)\n# [\'Use Application Commands\', \'Use Voice Activity\']\n```\n\nThat\'s about all there is to it. alianator does one thing and does it well.\n\n## License\n\nalianator is released under the [MIT License](https://github.com/celsiusnarhwal/alianator/blob/master/LICENSE.md).\n',
    'author': 'celsius narhwal',
    'author_email': 'celsiusnarhwal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/celsiusnarhwal/alianator',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
