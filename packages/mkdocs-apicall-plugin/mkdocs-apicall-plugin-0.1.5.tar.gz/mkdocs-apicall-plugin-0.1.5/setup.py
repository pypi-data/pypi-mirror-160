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
    'version': '0.1.5',
    'description': 'Auto-generate code samples to make API calls',
    'long_description': '# mkdocs-apicall-plugin\n\n[![Build](https://github.com/asiffer/mkdocs-apicall-plugin/actions/workflows/build.yaml/badge.svg)](https://github.com/asiffer/mkdocs-apicall-plugin/actions/workflows/build.yaml)\n[![Publish](https://github.com/asiffer/mkdocs-apicall-plugin/actions/workflows/publish.yaml/badge.svg)](https://github.com/asiffer/mkdocs-apicall-plugin/actions/workflows/publish.yaml)\n[![PyPI version](https://badge.fury.io/py/mkdocs-apicall-plugin.svg)](https://badge.fury.io/py/mkdocs-apicall-plugin)\n\nAuto-generate code samples to make API calls\n\n![](assets/example3.gif)\n\n## Installation\n\n```shell\npip install mkdocs-apicall-plugin\n```\n\nThis plugin works with the [material](https://squidfunk.github.io/mkdocs-material/) theme and is built on top of the [`tabbed`](https://facelessuser.github.io/pymdown-extensions/extensions/tabbed/) and [`superfenced`](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/) extensions from PyMdown. Enable the extensions and the plugin in your `mkdocs.yml`:\n\n```yaml\ntheme:\n  name: material\n\nmarkdown_extensions:\n  - pymdownx.superfences\n  - pymdownx.tabbed:\n      alternate_style: true\n\nplugins:\n  - apicall\n```\n\n\n## Syntax\n\nThe syntax is given below. Basically it may look like a classical HTTP request message.\n\n```md\n@@@ <METHOD> <PATH> [<PAYLOAD>]\n    [<HEADER-KEY>: <HEADER-VALUE>]\n    [<HEADER-KEY>: <HEADER-VALUE>]\n```\n\nThe method and the paths are both mandatory. \nOne can append a payload (only a json for the moment) to the first line.\nThe following lines are extra indented HTTP headers.\n\n## Configuration\n\nThe plugin supports few options:\n\n**`line_length`** [`int`] is the maximum length of a line of code before splitting into several lines.\n\n**`icons`** [`bool`] activates language icons. You must add the following extensions:\n\n```yaml\nmarkdown_extensions:\n  # ...   \n  - attr_list\n  - pymdownx.emoji:\n      emoji_index: !!python/name:materialx.emoji.twemoji\n      emoji_generator: !!python/name:materialx.emoji.to_svg\n```\n\n\n**`languages`** [`list`] filters the languages to display (show all by default). The order is also taken into account. The term *language* is clearly a misuse as it rather refers to a *way to make the API call* (so we may have `curl`, `wget` along with `typescript` for example). Currently **3 languages** are supported: `curl`, `python` and `javascript`.\n\nAs an example you may have:\n\n```yaml\nplugins:\n  - apicall:\n      line_length: 90\n      icons: true\n      languages:\n        - curl\n        - python\n        - javascript\n```\n\nYou can also pass extra configuration to a language by adding some sub-keys:\n\n```yaml\nplugins:\n  - apicall:\n      line_length: 90\n      icons: true\n      languages:\n        - curl:\n            options:\n              - "-s"\n        - python\n        - javascript\n```\n\nCurrently only `curl` supports the `options` sub-key to insert some CLI options.\n\n## Contributing\n\nObviously, we need to dev more *languages*  and increase the number of features: HTTP options, language options, code formatting...\n\n### How?\n\nOpen an issue, we may possibly discuss about the requested feature and if we are OK, you can create a branch and submit PR.\n\n### Developing a new language\n\nTo add a new language, you have to create a new source code file inside the [mkdocs_apicall_plugin/](https://github.com/asiffer/mkdocs-apicall-plugin/tree/master/mkdocs_apicall_plugin) folder.\n\nBasically a language looks as follows:\n\n```python\nfrom .abstract import APICall\n\n\nclass NewAPICall(APICall):\n    # [unique] name of the language. This is what is displayed\n    # in the tabs\n    name: str = "new"\n    # material mkdocs icons (see https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/)\n    icon: str = ":material-web:" \n    # Pygments language for syntax highlighting\n    # (see https://pygments.org/languages/)\n    lang: str = "shell" \n    # Indentation when the call is wrapped into several lines\n    # This is just for internal use (so it depends on how you\n    # code the language)\n    indent: str = " " * 5\n\n    def render_code(self) -> str:\n      """Single function to implement. It must return the raw \n      string that will be encapsulated in code blocks and tabs.\n      """\n      # TODO\n```\n\nSo, you must implement a subclass of `APICall` and notably the `render_code` method. This method returns only the code as string, \nas you may write in your favorite editor.\n\nYou have access to several attributes:\n\n| Attribute          | Type                  | Details                                                                               |\n| ------------------ | --------------------- | ------------------------------------------------------------------------------------- |\n| `_method`          | `abstract.HttpMethod` | Like `GET` or `POST`. This is always uppercase                                        |\n| `_url`             | `str`                 | API endpoint to reach                                                                 |\n| `_headers`         | `Dict[str, Any]`      | HTTP headers                                                                          |\n| `_body`            | `str`                 | Raw body as string (as it is written in the API call within the markdown source file) |\n| `_max_line_length` | `int`                 | Maximum line length desired                                                           |\n| `_print_icon`      | `bool`                | Whether the icon will be printed (normally it does have impact on your dev)           |\n| `_language_config` | `dict`                | Language specific configuration                                                       |\n\n:warning: You are responsible of the possible default values of the`_language_config` attribute.\n\n:warning: You are encouraged to render code differently according to the value of `_max_line_length`. One may imagine at least an *inline* and a *multiline* rendering.',
    'author': 'Alban Siffer',
    'author_email': 'alban@situation.sh',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/asiffer/mkdocs-apicall-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
