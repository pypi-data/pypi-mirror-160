# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daglib', 'daglib.core', 'daglib.utils']

package_data = \
{'': ['*']}

install_requires = \
['dask>=2022.6.0,<2023.0.0',
 'duckdb>=0.4.0,<0.5.0',
 'fastavro>=1.5.3,<2.0.0',
 'numpy>=1.23.0,<2.0.0',
 'tenacity>=8.0.1,<9.0.0']

extras_require = \
{'graphviz': ['graphviz>=0.20,<0.21']}

setup_kwargs = {
    'name': 'daglib',
    'version': '0.3.2',
    'description': 'Lightweight DAG composition framework',
    'long_description': '# ⚗️ Daglib - Lightweight DAG composition framework\n\n[![PyPI version](https://badge.fury.io/py/daglib.svg)](https://badge.fury.io/py/daglib)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/daglib)](https://pypi.org/project/daglib/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/daglib.svg)](https://pypi.org/project/daglib/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue.svg)](https://mypy.readthedocs.io/en/stable/)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\nDaglib is a lightweight alternative to Airflow and other orchestration engines. It is meant to run on a single machine and comes with many great features out of the box like task I/O, dynamic task generation, and simple testing and deployment.\n\nIt can run as a standalone application or be embedded in another application to enable more complex use cases like event-driven workflows, conditional workflows, and more.\n\nSee documentation at https://mharrisb1.github.io/daglib/\n\n# Installation\n\n```shell\npip install daglib\n```\n\n# Create your first DAG\n\n\n```python\nimport daglib\n\ndag = daglib.Dag()\n\n\n@dag.task()\ndef task_1a():\n    return "Hello"\n\n\n@dag.task()\ndef task_1b():\n    return "world!"\n\n\n@dag.task(final=True)\ndef tassk_2(task_1a, task_1b):\n    print(f"{task_1a}, {task_1b}")\n\n\ndag.run()\n```\n\n    Hello, world!\n\n\n# Beyond the "Hello, world!" example\n\nFor a more involved example, we will create a small ETL pipeline that takes data from four source tables and creates a single reporting table. The data is driver-level information from the current 2022 Formula 1 season. The output will be a pivot table for team-level metrics.\n\n## Source Tables\n\n1. Team - Which team the driver belongs to for the season\n2. Points - Current total Driver\'s World Championship points for each driver for the season\n3. Wins - Current number of wins for each driver for the season\n4. Podiums - Current number of times the driver finished in the top 3 for the season\n\n\n```python\nimport pandas as pd\nimport daglib\n\n# Ignore. Used to render the DataFrame correctly in the README\npd.set_option("display.notebook_repr_html", False)\n\ndag = daglib.Dag()\n\n\n@dag.task()\ndef team():\n    return pd.DataFrame(dict(\n        driver=["Max", "Charles", "Lewis", "Sergio", "Carlos", "George"],\n        team=["Red Bull", "Ferrari", "Mercedes", "Red Bull", "Ferrari", "Mercedes"],\n    )).set_index("driver")\n\n\n@dag.task()\ndef points():\n    return pd.DataFrame(dict(\n        driver=["Max", "Charles", "Lewis", "Sergio", "Carlos", "George"],\n        points=[175, 126, 77, 129, 102, 111]\n    )).set_index("driver")\n\n\n@dag.task()\ndef wins():\n    return pd.DataFrame(dict(\n        driver=["Max", "Charles", "Lewis", "Sergio", "Carlos", "George"],\n        wins=[6, 2, 0, 1, 0, 0]\n    )).set_index("driver")\n\n\n@dag.task()\ndef podiums():\n    return pd.DataFrame(dict(\n        driver=["Max", "Charles", "Lewis", "Sergio", "Carlos", "George"],\n        podiums=[7, 4, 2, 5, 5, 3]\n    )).set_index("driver")\n\n\n@dag.task()\ndef driver_metrics(team, points, wins, podiums):\n    return team.join(points).join(wins).join(podiums)\n\n\n@dag.task(final=True)\ndef team_metrics(driver_metrics):\n    return driver_metrics.groupby("team").sum().sort_values("points", ascending=False)\n\n\ndag.run()\n```\n\n\n\n\n              points  wins  podiums\n    team\n    Red Bull     304     7       12\n    Ferrari      228     2        9\n    Mercedes     188     0        5\n\n\n\n## Task Graph Visualization\n\nThe DAG we created above will create a task graph that looks like the following\n\n![task graph](https://storage.googleapis.com/daglib-image-assets/example-dag.png)\n',
    'author': 'Michael Harris',
    'author_email': 'mharris@luabase.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mharrisb1/daglib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
