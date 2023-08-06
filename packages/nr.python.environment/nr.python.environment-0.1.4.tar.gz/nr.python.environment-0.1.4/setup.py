# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['environment']

package_data = \
{'': ['*']}

install_requires = \
['setuptools>=33.0.0']

setup_kwargs = {
    'name': 'nr.python.environment',
    'version': '0.1.4',
    'description': '',
    'long_description': '# nr.python.environment\n\nUtilities to work with Python environments.\n\n### API\n\n*function* __`nr.python.environment.distributions.get_distributions(): Dict[str, Distribution]`__\n\nReturns all distributions that can be found in the current Python environment. This can be useful to build a dependency\ngraph or to collect the license of all packages used.\n\n### CLI\n\n__`python -m nr.python.environment.distributions`__\n\nProduce a CSV or JSON list of all distributions in the current Python environment. It can be used for\nexample to get an overview of the different types of licenses for the Python packages installed in an environment:\n\n    $ python -m nr.python.environment.distributions  | jq .license_name -r | sort | uniq\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
