# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tabeline', 'tabeline._expression']

package_data = \
{'': ['*']}

install_requires = \
['parsita>=1.7.0,<2.0.0',
 'polars>=0.13.11,<0.14.0',
 'typing_extensions>=4.3.0,<5.0.0']

extras_require = \
{'pandas': ['pandas>=1.4.3,<2.0.0', 'pyarrow>=8.0.0,<9.0.0']}

setup_kwargs = {
    'name': 'tabeline',
    'version': '0.1.0',
    'description': 'A data table and data grammar library',
    'long_description': '# Tabeline\n\nTabeline is a data table and data grammar library. You write the expressions in strings and supply them to methods on the `DataTable` class. The  strings are parsed by Parsita and converted into Polars for execution.\n\nTabeline draws inspiration from dplyr, the data grammar of R\'s tidyverse, especially for its methods names. The `filter`, `mutate`, `group`, and `summarize` methods should all feel familiar. But Tabeline is as proper a Python library as can be, using methods instead of pipes, like is standard in R. \n\nTabeline uses Polars under the hood, but adds a lot of handling of edge cases from Polars, which otherwise result in crashes or behavior that is not type stable.\n\nSee the [Documentation](htps://tabeline.drhagen.com) for the full user guide.\n\n## Installation\n\nIt is recommended to install Tabeline from PyPI using `pip`.\n\n```shell\npip install tabeline\n```\n\n## Motivating example\n\n```python\nfrom tabeline import DataTable\n\n# Construct a table using clean syntax\n# from_csv, from_pandas, and from_polars are also available \ntable = DataTable(\n    id=[0, 0, 0, 0, 1, 1, 1, 1, 1],\n    t=[0, 6, 12, 24, 0, 6, 12, 24, 48],\n    y=[0, 2, 3, 1, 0, 4, 3, 2, 1],\n)\n\n# Use data grammar methods and string expressions to define\n# transformed data tables\nanalysis = (\n    table\n    .filter("t <= 24")\n    .group("id")\n    .summarize(auc="trapz(t, y)")\n)\n\nprint(analysis)\n# shape: (2, 2)\n# ┌─────┬──────┐\n# │ id  ┆ auc  │\n# │ --- ┆ ---  │\n# │ i64 ┆ f64  │\n# ╞═════╪══════╡\n# │ 0   ┆ 45.0 │\n# ├╌╌╌╌╌┼╌╌╌╌╌╌┤\n# │ 1   ┆ 63.0 │\n# └─────┴──────┘\n```\n',
    'author': 'David Hagen',
    'author_email': 'david@drhagen.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/drhagen/parsita',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
