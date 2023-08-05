# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dash_callbackmanager', 'dash_callbackmanager.tests']

package_data = \
{'': ['*']}

install_requires = \
['dash<4.0.0']

setup_kwargs = {
    'name': 'dash-callbackmanager',
    'version': '2.0.0',
    'description': 'Dash callback manager, group callbacks easier within code.',
    'long_description': '# dash-callbackmanager\n\nAs your dash application grows the management of callbacks becomes a bit of an overhead. The \ncallback manager allows you to bundle collections of dash callbacks together allowing you to easily keep your\n`app.py` clean.\n\n## Installation:\n```shell\npip install dash-callbackmanager\n```\n\n## Usage:\nThe callback manager allows you to easily slip out the callbacks into separate files.\n\n```python\n# callbacks.py\n\nfrom dash_callbackmanager import CallbackManager\n\nmanager = CallbackManager()\n\n@manger.callback()\ndef my_callback(Output("element", "children"), Input("other-element", "value")):\n    ...\n```\n\n```python \n# app.py\nfrom dash import Dash\nfrom .callbacks import manager\n\napp = Dash(__name__)\n\nmanager.register(app)\n```',
    'author': 'Matt Seymour',
    'author_email': 'matt@enveloprisk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/envelop-risk/dash-callbackmanager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11.0',
}


setup(**setup_kwargs)
