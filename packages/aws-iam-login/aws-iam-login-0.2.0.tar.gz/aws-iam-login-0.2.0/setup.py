# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_iam_login', 'aws_iam_login.actions']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.24.11,<2.0.0', 'click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['aws-iam-login = aws_iam_login:main']}

setup_kwargs = {
    'name': 'aws-iam-login',
    'version': '0.2.0',
    'description': 'Configures STS credentials using a MFA authenticated session.',
    'long_description': '# AWS IAM Login\n\n`aws-iam-login` allows you to login using MFA as the IAM user itself. Once logged in your temporary credentials are\nstored in the `~/.aws/credentials` file for re-use.\n\n## Configuration\n\nYou will need to configure your roles and IAM User credentials in the same places as you are used to. So in your\n`~/.aws/credentials` file. To make this process as easy as possible you could use the following command:\n\n```bash\naws-iam-login my-profile init\n```\n\nThis command will fetch the ARN of the caller identity. Based on this identity we will determin the `username` and\n`mfa_serial` of the IAM User. These will then be stored in the `~/.aws/credentials` file. For example:\n\n```ini\n[my-profile]\naws_access_key_id = XXXXXXX\naws_secret_access_key = XXXXXXXXXXXXXXXXXXXXXXXXXXXX\nmfa_serial = arn:aws:iam::111122223333:mfa/my-iam-user\nusername = my-iam-user\n```\n\nThe only addition is the `username` and `mfa_serial` fields.\n\n### AWS Least privileged\n\nAssuming you have an IAM User that is already configured you will need the following permissions to use `aws-iam-login`:\n\n```json\n{\n  "Version": "2012-10-17",\n  "Statement": [\n    {\n      "Sid": "AllowSessionTokeUsingMFA",\n      "Effect": "Allow",\n      "Action": [\n        "sts:GetSessionToken"\n      ],\n      "Resource": "*",\n      "Condition": {\n        "BoolIfExists": {\n          "aws:MultiFactorAuthPresent": "true"\n        }\n      }\n    },\n    {\n      "Sid": "AllowAccessKeyRotation",\n      "Effect": "Allow",\n      "Action": [\n        "iam:ListAccessKeys",\n        "iam:CreateAccessKey",\n        "iam:UpdateAccessKey",\n        "iam:DeleteAccessKey"\n      ],\n      "Resource": [\n        "arn:aws:iam::111122223333:user/${aws:username}"\n      ]\n    }\n  ]\n}\n```\n\n## Usage\n\nWhen you want to make use of the MFA authenticated session of a configured profile. You will need to configure the\nfollowing:\n\n```ini\n[profile my-role-1]\nrole_arn = arn:aws:iam::111122223333:role/my-role-1\nsource_profile = my-profile-sts\nregion = eu-west-1\n```\n\nThen when you perform your AWS cli calls you can use the `AWS_PROFILE=my-role-1` as you are used to. But the first time  it will fail. The reason for this is that the `my-profile-sts` source profile does not exist (or the credentials are expired).\nPerform the following command to login, this command will ask for your MFA Token:\n\n```bash\naws-iam-login my-profile\n```\n\nThis authenticates against the AWS API and request temporary credentials from AWS using your MFA Token. These credentials are then stored as `<profile-name>-sts`.\nSo the next time you use `AWS_PROFILE=my-role-1` the credentials will be present and not expired.\n\nBecause you are already authenticated using MFA there is no need to provide an MFA token when you assume the role.\nWhen you switch a lot between roles you really benefit from not having to type your MFA token each time you switch.\n\n### Rotating your AccessKey and SecretAccessKey\n\nIt is advised to rotate your credentials regularly. `aws-iam-login` can help with that! By executing the following command:\n\n```bash\naws-iam-login my-rofile rotate\n```\n\nThis command will execute the following actions:\n\n1. List all available keys for the user, when 1 key is active rotation is possible!\n2. Create a new AccessKey and SecretAccessKey.\n3. Use the newly created keys to deactivate the old keys.\n4. Write the new keys to the `~/.aws/configuration` file.\n5. Delete the old keys.\n',
    'author': 'Joris Conijn',
    'author_email': 'jorisconijn@binx.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
