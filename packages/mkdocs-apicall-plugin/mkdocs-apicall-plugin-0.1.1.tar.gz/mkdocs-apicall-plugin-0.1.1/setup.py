# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_apicall_plugin']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.6.0,<23.0.0',
 'mkdocs-material>=8.3.9,<9.0.0',
 'mkdocs>=1.3.1,<2.0.0']

entry_points = \
{'mkdocs.plugins': ['apicall = mkdocs_apicall_plugin.main:APICallPlugin']}

setup_kwargs = {
    'name': 'mkdocs-apicall-plugin',
    'version': '0.1.1',
    'description': 'Automatically insert code snippets to run API calls',
    'long_description': '# mkdocs-apicall-plugin\n\n[![CI](https://github.com/asiffer/mkdocs-apicall-plugin/actions/workflows/ci.yaml/badge.svg)](https://github.com/asiffer/mkdocs-apicall-plugin/actions/workflows/ci.yaml)\n\nAutomatically insert code snippets to run API calls\n\n```md\n## Simple call \n\n@@@ GET /object/list\n\n\n## Single header\n\n@@@ GET /object/list\n    Accept: application/json\n\n\n## Full call\n\n@@@ POST /data/blob {"a": "b"}\n    Accept: application/json\n    Content-Type: application/json\n    Authorization: Bearer 4P1k3y\n```\n\n![](assets/example.gif)\n\n## Installation\n\n```shell\npip install mkdocs-apicall-plugin\n```\n\nThis plugin works with the [material](https://squidfunk.github.io/mkdocs-material/) theme and is built on top of the [`tabbed`](https://facelessuser.github.io/pymdown-extensions/extensions/tabbed/) and [`superfenced`](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/) extensions from PyMdown. Enable the extensions and the plugin in your `mkdocs.yml`:\n\n```yaml\ntheme:\n  name: material\n\nmarkdown_extensions:\n  - pymdownx.superfences\n  - pymdownx.tabbed:\n      alternate_style: true\n\nplugins:\n  - apicall\n```\n\n\n## Syntax\n\nThe syntax is given below. Basically it may look like a classical HTTP request message.\n\n```ini\n@@@ <METHOD> <PATH> [<PAYLOAD>]\n    [<HEADER-KEY>: <HEADER-VALUE>]\n    [<HEADER-KEY>: <HEADER-VALUE>]\n```\n\nThe method and the paths are both mandatory. \nOne can append a payload (only a json for the moment) to the first line.\nThe following lines are extra indented HTTP headers.\n\n## Configuration\n\nThe plugin supports few options:\n\n**`line_length`** [`int`] is the maximum length of a line of code before splitting into several lines.\n\n**`icons`** [`bool`] activates language icons. You must add the following extensions:\n\n```yaml\nmarkdown_extensions:\n  # ...   \n  - attr_list\n  - pymdownx.emoji:\n      emoji_index: !!python/name:materialx.emoji.twemoji\n      emoji_generator: !!python/name:materialx.emoji.to_svg\n```\n\n\n**`languages`** [`list`] filters the languages to display (show all by default). The order is also taken into account. The term *language* is clearly a misuse as it rather refers to a *way to make the API call* (so we may have `curl`, `wget` along with `typescript` for example). Currently **3 languages** are supported: `curl`, `python` and `javascript`.\n\nAs an example you may have:\n\n```yaml\nplugins:\n  - apicall:\n      line_length: 90\n      icons: true\n      languages:\n        - curl\n        - python\n        - javascript\n```\n\n## Contributing\n\nObviously, we need to dev more *languages* !',
    'author': 'Alban Siffer',
    'author_email': 'alban@situation.sh',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/asiffer/mkdocs-apicall-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
