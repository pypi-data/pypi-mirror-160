# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cloud_connectors',
 'cloud_connectors.aws_connector',
 'cloud_connectors.azure_connector',
 'cloud_connectors.common',
 'cloud_connectors.common.cli',
 'cloud_connectors.common.cli.commands',
 'cloud_connectors.gcp_connector']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'backoff>=2.1.2,<3.0.0',
 'censys>=2.1.2,<3.0.0',
 'inquirerpy>=0.3.3,<0.4.0',
 'polling2>=0.5.0,<0.6.0',
 'pydantic[email,dotenv]>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.4.4,<13.0.0']

extras_require = \
{':python_version <= "3.8"': ['importlib-metadata'],
 'aws': ['boto3>=1.24.2,<2.0.0',
         'boto3-stubs[route53,elb,ec2,apigateway,ecs,elbv2,s3,route53domains,secretsmanager,rds,apigatewayv2]>=1.24.11,<2.0.0'],
 'azure': ['azure-cli>=2.34.1,<3.0.0',
           'azure-common>=1.1.28,<2.0.0',
           'azure-core>=1.22.0,<2.0.0',
           'azure-identity>=1.7.1,<2.0.0',
           'azure-mgmt-compute>=25.0.0,<25.1.0',
           'azure-mgmt-containerinstance>=9.1.0,<10.0.0',
           'azure-mgmt-core>=1.3.0,<2.0.0',
           'azure-mgmt-dns>=8.0.0,<9.0.0',
           'azure-mgmt-network>=19.3.0,<20.0.0',
           'azure-mgmt-resource==20.0.0',
           'azure-mgmt-resource==20.0.0',
           'azure-mgmt-sql>=3.0.1,<4.0.0',
           'azure-mgmt-storage>=19.1.0,<20.0.0',
           'azure-storage-blob>=12.9.0,<13.0.0'],
 'gcp': ['google-auth>=2.6.0,<3.0.0',
         'google-cloud-resource-manager>=1.4.1,<2.0.0',
         'google-cloud-securitycenter>=1.9.0,<2.0.0']}

entry_points = \
{'console_scripts': ['censys-cc = censys.cloud_connectors.common.cli:main']}

setup_kwargs = {
    'name': 'censys-cloud-connectors',
    'version': '3.0.1b1',
    'description': 'The Censys Unified Cloud Connector is a standalone connector that gathers assets from various cloud providers and stores them in Censys ASM.',
    'long_description': None,
    'author': 'Censys, Inc.',
    'author_email': 'support@censys.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
