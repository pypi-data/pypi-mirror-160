# nr.python.environment

Utilities to work with Python environments.

### API

*function* __`nr.python.environment.distributions.get_distributions(): Dict[str, Distribution]`__

Returns all distributions that can be found in the current Python environment. This can be useful to build a dependency
graph or to collect the license of all packages used.

### CLI

__`python -m nr.python.environment.distributions`__

Produce a CSV or JSON list of all distributions in the current Python environment. It can be used for
example to get an overview of the different types of licenses for the Python packages installed in an environment:

    $ python -m nr.python.environment.distributions  | jq .license_name -r | sort | uniq
