# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arq_prometheus']

package_data = \
{'': ['*']}

install_requires = \
['arq>=0.22,<0.23', 'prometheus-client>=0.14.1,<0.15.0']

setup_kwargs = {
    'name': 'arq-prometheus',
    'version': '0.2.0',
    'description': 'Prometheus metrics for arq job queues',
    'long_description': '# Arq-prometheus\n\n![Build status](https://github.com/kpn/arq-prometheus/actions/workflows/test.yaml/badge.svg?branch=master)\n[![PyPI Package latest release](https://img.shields.io/pypi/v/arq-prometheus.svg?style=flat-square)](https://pypi.org/project/commitizen/)\n[![PyPI Package download count (per month)](https://img.shields.io/pypi/dm/arq-prometheus?style=flat-square)](https://pypi.org/project/arq-prometheus/)\n[![Supported versions](https://img.shields.io/pypi/pyversions/arq-prometheus.svg?style=flat-square)](https://pypi.org/project/commitizen/)\n[![Codecov](https://img.shields.io/codecov/c/github/kpn/arq-prometheus.svg?style=flat-square)](https://codecov.io/gh/kpn/arq-prometheus)\n\n\nPrometheus metrics for [arq](https://github.com/samuelcolvin/arq)\n\n⚠️ WARNING! This is a project in alpha phase ⚠️\n\n## Installation\n\n[Pip](https://pip.pypa.io/en/stable/)\n\n```sh\npip install -U arq-prometheus\n```\n\n[Poetry](https://python-poetry.org/)\n\n```sh\npoetry add arq-prometheus\n```\n\n## Description\n\nThe metrics exposed are the same as the health check.\n\n| Metric name             | Description                      |\n| ----------------------- | -------------------------------- |\n| `arq_jobs_completed`    | The number of jobs completed     |\n| `arq_jobs_failed`       | The total number of errored jobs |\n| `arq_jobs_retried`      | The total number of retried jobs |\n| `arq_ongoing_jobs`      | The number of jobs in progress   |\n| `arq_queued_inprogress` | The number of jobs in progress   |\n\nWhen working with `arq` I found some limitations, it was specially hard to get access to\nthe worker in order to retrieve information like the `queue_name` or `health_check_key`.\nThe startup and shutdown functions only make available a `ctx` with the redis connection.\nThis means that if you provide a custom `queue_name` or `health_check_key`, you will\nalso have to provide them to `ArqPrometheusMetrics`.\n\n## Usage\n\n````python\n# example_worker.py\nfrom arq_prometheus import ArqPrometheusMetrics\n\nasync def startup(ctx):\n    arq_prometheus = ArqPrometheusMetrics(ctx, delay=delay)\n    ctx["arq_prometheus"] = await arq_prometheus.start()\n\nasync def shutdown(ctx):\n    await ctx["arq_prometheus"].stop()\n\nclass WorkerSettings:\n    on_startup = startup\n    on_shutdown = shutdown\n    function = []  # your arq jobs\n    ... # other settings\n\n````\n\nStart your arq worker,\n\n```sh\narq example_worker.WorkerSettings\n```\n\nMake request to `localhost:8081` (or open in browser).\n\n```sh\ncurl localhost:8081\n```\n\n\n## Arguments\n\n- `ctx: dict`: arq context\n- `queue_name: str = default_queue_name`: name of the arq queue\n- `health_check_key: Optional[str] = None`: arq health key\n- `delay: datetime.timedelta = datetime.timedelta(seconds=5)`: a datetime.timedelta\n- `enable_webserver: bool = True`: set to True if you want a web server exposing the metrics\n- `addr: str = "0.0.0.0"`: webserver address\n- `port: int = 8081`: webserver port\n- `registry: prom.CollectorRegistry = prom.REGISTRY`: the prometheus registry, usually you do not have to override this',
    'author': 'Santiago Fraire Willemoes',
    'author_email': 'santiago.fraire@kpn.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
