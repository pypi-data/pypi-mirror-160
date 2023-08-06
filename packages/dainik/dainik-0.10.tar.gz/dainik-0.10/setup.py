# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dainik']

package_data = \
{'': ['*'], 'dainik': ['yql/.git']}

install_requires = \
['Jinja2==3.0.3', 'nbox>=0.9.14rc28,<0.10.0']

setup_kwargs = {
    'name': 'dainik',
    'version': '0.10',
    'description': 'Client library for working with nimblebox LMAO',
    'long_description': '# Dainik\n\n`Dainik` is a client library for NimbleBox.ai LMAO (Logging, Monitoring, Alerts and Observability) service.\n\n## Usage\n\n```python\nfrom dainik import Dainik\n\n# initialise the client object\ndk = Dainik()\n\n# initialise the run\ndk.init(\n  "california",\n  config = {\n    "model_name": "qual",\n    "config": {\n      "batch_size": 32,\n      "n_steps": n_steps,\n      "optimizer": "adam",\n    }\n  },\n)\n\nfor epoch in range(10):\n  log = {\n    "loss": 1 / epoch,\n    "accuracy": epoch,\n  }\n  dk.log(log, step = epoch)\n\n  # optionally log metrics directly\n  dk.metrics.f1_score(\n    x = [[1, 2, 3]],\n    y = [[1, 2, 1]],\n    step = epoch\n  )\n\n  # log files for tracking as well, wildcards work as well!\n  dk.save_files([f"./checkpoint-{epoch}/*"])\n\ndk.end() # send signal to sleep\n```\n\n## Dev\n\nDue to the current structure the source code for this is only available for NimbleBox.ai engineers. This is spun out of a much larger monorepo which contains the logic for server and client together which helps us work on this faster. \n',
    'author': 'yashbonde',
    'author_email': 'bonde.yash97@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NimbleBoxAI/nbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
