# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['certbot_aws_store']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'b-dynamodb-common>=0.4.0,<0.5.0',
 'certbot-route53>=0.2.0,<0.3.0',
 'certbot>=1.29.0,<2.0.0',
 'compose-x-common>=1.0.4,<2.0.0',
 'pyOpenSSL>=22.0.0,<23.0.0',
 'pynamodb>=5.2.1,<6.0.0']

entry_points = \
{'console_scripts': ['certbot-aws-store = '
                     'certbot_aws_store.cli:cli_entrypoint']}

setup_kwargs = {
    'name': 'certbot-aws-store',
    'version': '0.2.0',
    'description': "Generate Let's Encrypt certificates and store into AWS",
    'long_description': '==================================\ncertbot-aws-store\n==================================\n\nWrapper tool / function around certbot + route53 that allows to request new certificates, and store them in AWS.\n\nFeatures\n\n* Store Let\'s Encrypt certificates in AWS SecretsManager (default) and S3 (optional)\n* Keep track of ACME account configuration and store securely in AWS SecretsManager\n* Keep track of certificates issued and stored in account via DynamoDB\n\nPre-Requisites\n================\n\n* A function AWS Account and credentials to make API calls\n* Access to DynamoDB + SecretsManager + S3 (optional)\n\nWe recommend to create the dynamodb table using the ``certbot-store-registry.template`` CFN template, otherwise\ncertbot-aws-store will attempt to create it programmatically.\n\nThe needed RCU/WCU should be 5/5 (default) or lower.\n\nInstall\n=========\n\n.. code-block::\n\n    pip install certbot-aws-store --user\n\n    python3 -m venv venv\n    source venv/bin/activate\n    pip install pip -U; pip install certbot-aws-store\n\nUsage\n======\n\nAs a CLI\n----------\n\n\n.. code-block::\n\n    usage: Certbot store wrapper [-h] --secret SECRET --domain DOMAIN --email EMAIL [--register-to-acm] [--dry-run] [--override-folder OVERRIDE_FOLDER] [--profile PROFILE] [--s3-backend-bucket-name BUCKETNAME]\n                                 [--s3-backend-prefix-key S3_PREFIX_KEY] [--split-secrets] [--secretsmanager-backend-prefix-key SECRETS_PREFIXKEY]\n\n    optional arguments:\n      -h, --help            show this help message and exit\n      --secret SECRET, --secret-store-arn SECRET\n                            ACME Configuration secret name/ARN\n      --domain DOMAIN       Domain name for the certificate to create\n      --email EMAIL         Email for the account and ToS\n      --register-to-acm     Creates|Updates certificate in ACM\n      --dry-run             By default, use ACME Staging.\n      --override-folder OVERRIDE_FOLDER\n                            Use an existing certbot folder\n      --profile PROFILE     AWS Profile to use for API requests\n      --s3-backend-bucket-name BUCKETNAME\n                            S3 bucket to store the certificate files into\n      --s3-backend-prefix-key S3_PREFIX_KEY\n                            S3 Prefix path to store the certificates\n      --split-secrets       If set, each certificate file gets their own secret in Secrets Manager\n      --secretsmanager-backend-prefix-key SECRETS_PREFIXKEY\n                            SecretsManager prefix for secret name\n\nExample\n--------\n\n.. code-block::\n\n    certbot-aws-store --secret dev-acme-store --override-folder certbot-store \\\n     --email john@ews-network.net \\\n    --domain test-local-0005.bdd-testing.compose-x.io \\\n    --s3-backend-bucket-name dev-test-bucket\n\n\nInspiration\n=============\n\nLet\'s Encrypt + Certbot is a goto for anyone who wishes to have free SSL certificates to use in various places.\nBut then the certificates management, storage, backup and so on, still has to be done.\n\nThis is an attempt at automating the storage of certificates in AWS and the associated ACME account configuration\n(to avoid rate limiting).\n\nThis tool can be used as a CLI, and coming soon, an AWS Lambda Function or/and (coming soon) a CloudFormation resource.\nOnce installed on AWS, the registry will be automatically looked at daily to identify certificates that need to be\nrenewed and store the new values in appropriate places.\n\nHow does it work ?\n=====================\n\nOn the first time, if the ACME secret does not exist, we consider you never used ``certbot-aws-store`` before,\nand a new ACME account will be created, along with the certificate requested.\n\nOnce the certificate request is successfully completed, both the certificate and the ACME account details are saved\nto secrets manager (the certificate)\n\nUsing the dynamoDB "registry" table, we store the ARN to the various files stored in AWS, along with some metadata.\n\nFor example, the following represents a certificate stored in Secrets Manager, S3 and ACM\n\n.. code-block:: json\n\n    {\n     "hostname": "test-local-0106.bdd-testing.compose-x.io",\n     "account_id": "61811954",\n     "acmArn": "arn:aws:acm:eu-west-1:373709667837:certificate/82b3ab6f-5b53-4a3b-ab7d-ccd1ecb52255",\n     "endpoint": "acme-staging-v02.api.letsencrypt.org",\n     "expiry": "2022-10-20T22:38:59.000000+0000",\n     "s3Arn": {\n      "certChain": "arn:aws:s3:::dev-test-bucket::certbot/store/acme-staging-v02.api.letsencrypt.org/61812954/test-local-0106.bdd-testing.compose-x.io/chain.pem",\n      "fullChain": "arn:aws:s3:::dev-test-bucket::certbot/store/acme-staging-v02.api.letsencrypt.org/61812954/test-local-0106.bdd-testing.compose-x.io/fullchain.pem",\n      "privateKey": "arn:aws:s3:::dev-test-bucket::certbot/store/acme-staging-v02.api.letsencrypt.org/61812954/test-local-0106.bdd-testing.compose-x.io/privkey.pem",\n      "publicKey": "arn:aws:s3:::dev-test-bucket::certbot/store/acme-staging-v02.api.letsencrypt.org/61812954/test-local-0106.bdd-testing.compose-x.io/cert.pem"\n     },\n     "secretsmanagerArn": "arn:aws:secretsmanager:eu-west-1:373709667837:secret:certbot/store/acme-staging-v02.api.letsencrypt.org/61812954/test-local-0106.bdd-testing.compose-x.io-HpgyTD",\n     "secretsmanagerCertsArn": {}\n    }\n\nThe registry will be used in the future to evaluate / list the certificates that we have and decide whether or not\na certificate should be renewed.\n\nWhen stored in SecretsManager, we might implement a Lambda function to implement the rotation which would update\neverything, including S3.\n\n.. warning::\n\n    If you use ``--dry-run`` to use the ACME staging endpoint for testing, and request the same domain name as for\n    the production ACME endpoint, and store the certificate to ACM, the latest of the two updates the ACM certificate.\n',
    'author': 'John Preston',
    'author_email': 'john@ews-network.net',
    'maintainer': 'John Preston',
    'maintainer_email': 'john@ews-network.net',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
