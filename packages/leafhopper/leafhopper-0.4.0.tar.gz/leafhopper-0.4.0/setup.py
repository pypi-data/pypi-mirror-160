# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leafhopper', 'leafhopper.descriptors', 'leafhopper.descriptors.extra']

package_data = \
{'': ['*']}

install_requires = \
['pytablewriter[html]>=0.64.2,<0.65.0', 'tomli>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['leafhopper = leafhopper.main:main']}

setup_kwargs = {
    'name': 'leafhopper',
    'version': '0.4.0',
    'description': 'A command line tool for generating project dependencies table',
    'long_description': "# leafhopper\nDo you get asked by your employer to provide a list of open source libraries that you use in the project for legal review?\n\n`leafhopper` is a command line tool used for generating a table of dependencies for a project, including their licenses, so that you don't have to manually maintain such a list for every release of your project.\n\n# How it works\nThe tool parses the project descriptor, based on different project types (`poetry`/`maven`/`vcpkg` are supported currently), and generates a table of dependencies. When some critical information, such as license, is not available in the project descriptor, `leafhopper` will test if this is a github/sourceforge project and try loading relevant information from `github.com`/`sourceforge.net`.\n\n# Features\n* parse multiple different project types to generate a table of dependencies from them\n* load license information from github/sourceforge\n* support overriding the list of dependencies from the project descriptor when you cannot get correct information from the project descriptor\n* support customizing the output columns\n* multiple outout formats\n\n# Installation\n```\npip install leafhopper\n```\n\n# Usage\n```\nleafhopper /path/to/project/descriptor\n```\n\n## arguments\n* `--format`: the format of the output. Possible values are `markdown`/`html`/`json`/`latex`/`csv`. Default is `markdown`.\n* `--output`: the output file path. If not specified, the output will be printed to stdout.\n* `--columns`: the output table header columns. It is a comma separated string. Default value is `name,version,homepage,license,description`. You can change the order of columns or add empty columns by changing the value. For example, `name,license,homepage,component` add a new empty column called `component` and reorder the columns as well.\n* `--logging-level`: the logging level. Possible values are `debug`/`info`/`warning`/`error`/`critical`. Default is `info`. \n  * Set the logging level to above `info` (e.g. `error`) to supress non critical messages so that only table is printed to stdout (if no output file is specified).\n  * Set the logging level to `debug` to enable debug messages.\n* `--extra`: the file path to a JSON file path containing extra package information to override the information parsed from project descriptors. The `overrides` property in JSON file is an array of objects with the following properties (here is an [example](tests/data/extra.json)):\n  * `name`\n  * `version`, optional\n  * `license`, optional\n  * `homepage`, optional\n  * `description`, optional\n\n* `--help`: show the help message\n\n## examples\n1. extract `pyproject.toml` dependencies with markdown format and save it into `dependencies.md` file\n```\nleafhopper /path/to/pyproject.toml --output=dependencies.md\n```\n\n2. extract `pom.xml` dependencies with html format\n```\nleaphopper /path/to/pom.xml --format=html\n```\n\n3. suppress logging and output to stdout and use CLI tool [`glow`](https://github.com/charmbracelet/glow) to display it\n```\nleafhopper /path/to/vcpkg.json --format md --logging-level error | glow -\n```\n\n4. use custom columns to change the column order and add an empty column called `component`, which you can fill later on\n```\nleaphopper /path/to/pom.xml --columns name,component,version,license,homepage,description\n```\n\n5. use an extra JSON file to override the information parsed from project descriptors\n```\nleaphopper /path/to/pom.xml --extra=tests/data/extra.json\n```\n\n\n# Supported formats\n* markdown\n* LaTex\n* html\n* json\n* csv\n## sample output\n* markdown format output\n```markdown\n# Package Dependencies\n|      name       |version|           homepage            | license  |                               description                               |\n|-----------------|-------|-------------------------------|----------|-------------------------------------------------------------------------|\n|simdjson         |2.2.0  |https://simdjson.org/          |Apache-2.0|A extremely fast JSON library that can parse gigabytes of JSON per second|\n|pcre             |   8.45|https://www.pcre.org/          |          |Perl Compatible Regular Expressions                                      |\n|pugixml          |1.12.1 |https://github.com/zeux/pugixml|MIT       |Light-weight, simple and fast XML parser for C++ with XPath support      |\n|arrow            |8.0.0  |https://arrow.apache.org       |Apache-2.0|Cross-language development platform for in-memory analytics              |\n```\n\n# Supported project types\n* poetry project described by `pyproject.toml`\n    * https://python-poetry.org/docs/pyproject/    \n* maven project described by `pom.xml`\n    * https://maven.apache.org/pom.html\n    * `pom.xml` with or without Maven XML namespace are supported.\n* vcpkg project described by `vcpkg.json`\n    * https://vcpkg.readthedocs.io/en/latest/specifications/manifests/\n* more project types such as npm will be supported in the future\n\n\n# Changelog\n[Changelog](CHANGELOG.md)\n\n# Known issues\n* Some open source libraries, doesn't have the license information available in the project descriptor (or in `github.com`/`sourceforge.net`), and the cell will be blank and you have to manually fill it.\n\n# TODO\n* Support more project types, such as `npm`'s `package.json` and `pip`'s `requirements.txt`\n",
    'author': 'Yue Ni',
    'author_email': 'niyue.com@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/niyue/leafhopper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
