# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dainik']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2==3.0.3', 'nbox>=0.9.14rc28,<0.10.0']

setup_kwargs = {
    'name': 'dainik',
    'version': '0.5',
    'description': 'Client library for working with nimblebox LMAO',
    'long_description': "# nimblebox-lmao\n\nLogging, Monitoring, Alerting &amp; Observability\n\n## Usage\n\nFor protobuf generation:\n- `sh gen.sh` will generate all the required files, but will also (⚠️) overwrite your `lmao_server.py` file.\n- `sh update_proto.sh` to only update the proto message definitions\n\nFor running the server:\n- `python3 -m uvicorn:server app` to run the server, it will connect to the backend on it's own\n\nFor running the clients:\n- `python3 -m clients.new` will do a complete run which includes `init`, `on_log`, `on_save` and `on_train_end` APIs\n- `python3 -m clients.stat --help` will tell more about getting the data from the DB\n- `python3 -m clients.logs --help` will tell more about getting the logs from the DB\n\n## Dev\n\n```\ngit clone ...\ncd nimblebox-lmao/\ngit submodule init\ngit submodule update --remote\n```\n",
    'author': 'yashbonde',
    'author_email': 'bonde.yash97@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NimbleBoxAI/nbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
