# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sblue']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'sendinblue-logger',
    'version': '1.0.0',
    'description': "Send log messages to sendinblue's transactional email service.",
    'long_description': "## Description\nThis is a logging handler for Python's [logging](https://docs.python.org/3/library/logging.html) module to send log messages over [sendinblue](https://www.sendinblue.com/)'s transactional email service.\n\n## Installation\n```shell\n$ pip install sendinblue-logger\n```\n\n## Usage\n```python\nimport sblue\nimport logging\nimport os\n\nhandler = sblue.LoggingHandler(\n    level=logging.ERROR,\n    api_key=os.getenv('SENDINBLUE_API_KEY'),\n    from_email='sender-email@domain.com',\n    to_email='recipient-email@domain.com',\n)\n\nlogging.basicConfig(\n    filename='/home/user/project/project.log', \n    encoding='utf-8', \n    level=logging.DEBUG, \n    format='%(asctime)s - %(levelname)s: %(message)s',\n    handlers=(handler,)\n)\n```",
    'author': 'Cal Warhurst',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/calwarhurst/sendinblue-logger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
