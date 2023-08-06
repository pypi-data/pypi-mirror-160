# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['derive',
 'derive.integrations',
 'derive.log',
 'derive.metrics',
 'derive.metrics.metric',
 'derive.trace']

package_data = \
{'': ['*']}

install_requires = \
['configalchemy>=0.5.5,<0.6.0',
 'opentelemetry-api>=1.11.1,<2.0.0',
 'opentelemetry-sdk>=1.11.1,<2.0.0']

extras_require = \
{'otlp-aws-xray': ['opentelemetry-sdk-extension-aws>=2.0,<3.0',
                   'opentelemetry-propagator-aws-xray>=1.0,<2.0',
                   'opentelemetry-exporter-otlp>=1.11,<2.0',
                   'protobuf>=3.10,<4.0'],
 'requests': ['opentelemetry-instrumentation-requests==0.30b1']}

setup_kwargs = {
    'name': 'derive',
    'version': '0.2.0',
    'description': 'The Python Observability Toolkit',
    'long_description': '# Derive: The Python Observability Toolkit\n\n[![Tests Status](https://github.com/DeBankDeFi/derive/workflows/Tests/badge.svg?branch=main&event=push)](https://github.com/DeBankDeFi/derive/actions?query=workflow%3ATests+branch%3Amain+event%3Apush)\n[![codecov](https://codecov.io/gh/DeBankDeFi/derive/branch/main/graph/badge.svg?token=LUVTL8L1B8)](https://codecov.io/gh/DeBankDeFi/derive)\n[![Python Version](https://img.shields.io/pypi/pyversions/derive.svg)](https://pypi.org/project/derive/)\n## What is Derive?\n\nderive based on OpenTelemetry, Prometheus, and FluentBit \nis a pure configuration-oriented Python Observability Toolkit making your systems observable.\nBuilding your trace, logging, and metrics in a simple and easy way in your production and development Phase.\n\n## How to use Derive\n\n### Install\n\n```bash\npip install derive\n```\n\n### Documentation\n\n- [Usage](./docs/usage.md)\n\n',
    'author': 'DeBankDeFi',
    'author_email': 'sre@debank.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DeBankDeFi/derive',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.2,<4.0',
}


setup(**setup_kwargs)
