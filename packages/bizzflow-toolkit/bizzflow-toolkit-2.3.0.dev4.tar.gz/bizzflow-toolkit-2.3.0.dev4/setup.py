# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toolkit',
 'toolkit.base',
 'toolkit.dags',
 'toolkit.dags.helpers',
 'toolkit.executors',
 'toolkit.executors.base',
 'toolkit.executors.extractor',
 'toolkit.executors.transformation',
 'toolkit.executors.writer',
 'toolkit.managers',
 'toolkit.managers.component',
 'toolkit.managers.configuration',
 'toolkit.managers.configuration.v1',
 'toolkit.managers.configuration.v2',
 'toolkit.managers.credentials',
 'toolkit.managers.datamart',
 'toolkit.managers.file_storage',
 'toolkit.managers.sandbox',
 'toolkit.managers.storage',
 'toolkit.managers.vault',
 'toolkit.managers.worker',
 'toolkit.utils']

package_data = \
{'': ['*'], 'toolkit.managers.configuration': ['schemas/v1/*', 'schemas/v2/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'boto3<1.16',
 'cffi==1.14.0',
 'fabric>=2.5.0,<3.0.0',
 'invoke>=1.4.1,<2.0.0',
 'jsonschema>=3.2.0,<3.3.0',
 'paramiko>=2.7.2,<3.0.0',
 'pyodbc>=4.0.30,<5.0.0',
 'python3-openid>=3.2.0,<4.0.0',
 'redshift-connector>=2.0.907,<3.0.0',
 'retry_helper>=0.0.4,<0.0.5',
 'sqlparse>=0.4.1,<0.5.0',
 'statsd>=3.3.0,<4.0.0']

setup_kwargs = {
    'name': 'bizzflow-toolkit',
    'version': '2.3.0.dev4',
    'description': 'Bizzflow is ETL (extract - transform - load) template based on standard native cloud services. Supporting the three main cloud providers (Google Cloud Platform / Amazon AWS / MS Azure), it takes all the advantages. You pay only for services you really use. Perfect for teams who want to have direct relationship with their cloud provider. No matter if it is because of security or because you already have existing contract.',
    'long_description': '# Bizzflow R2 Toolkit\n\n![alt text][bizztreat-logo]\n\nBizzflow R2 Toolkit is a version 2 of Bizzflow ETL Pipeline template written mostly in Python, using [Apache Airflow](https://airflow.apache.org/) as a scheduler and job executor. Bizzflow is meant to work in cloud, meaning any of the major cloud providers ([Google Cloud Platform](https://cloud.google.com), [Amazon Web Services](https://aws.amazon.com) and [Microsoft Azure](https://azure.microsoft.com)). If you would like to implement Bizzflow solution in your cloud, do not hesitate to contact [Bizztreat admin](https://bizztreat.com).\n\n\n## Contributing\n\n- [Building base image](doc/building_base.md)\n- [Dependency management](doc/dependency_management.md)\n\n\n## Crossroads\n\n- [Bizzflow R2 Toolkit Documentation](doc/README.md)\n- [Installation](doc/README.md#installation)\n- [Python API Reference](https://bizztreat.gitlab.io/bizzflow/r2/toolkit/index.html)\n- [Bizztreat](https://bizztreat.com)\n\n## Installation\n\nSee [Installation instructions](doc/README.md#installation) for more information.\n\n## License\n\n**TODO:** To be decided yet.\n\nSee details in [LICENSE](./LICENSE).\n\n[bizztreat-logo]: ./doc/bizztreatlogo.png "Bizztreat Logo"\n',
    'author': 'Bizztreat',
    'author_email': 'owner@bizzflow.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.bizzflow.net/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
