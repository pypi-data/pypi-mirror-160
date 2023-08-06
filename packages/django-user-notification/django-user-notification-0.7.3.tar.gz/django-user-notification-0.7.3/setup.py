# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notification', 'notification.backends', 'notification.migrations']

package_data = \
{'': ['*'], 'notification': ['templates/*']}

install_requires = \
['django>=3.2', 'requests>=2.27.1,<3.0.0']

extras_require = \
{'aliyunsms': ['alibabacloud-dysmsapi20170525>=2.0.16'],
 'channels': ['channels>=3.0.4']}

setup_kwargs = {
    'name': 'django-user-notification',
    'version': '0.7.3',
    'description': 'Django message notification package',
    'long_description': '# Django user notification\n\n[![GitHub license](https://img.shields.io/github/license/anyidea/django-user-notification)](https://github.com/anyidea/django-user-notification/blob/master/LICENSE)\n[![pypi-version](https://img.shields.io/pypi/v/django-user-notification.svg)](https://pypi.python.org/pypi/django-user-notification)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-user-notification)\n[![PyPI - Django Version](https://img.shields.io/badge/django-%3E%3D3.1-44B78B)](https://www.djangoproject.com/)\n[![Build Status](https://app.travis-ci.com/anyidea/django-user-notification.svg?branch=master)](https://app.travis-ci.com/anyidea/django-user-notification)\n\n\nOverview\n-----\nDjango user notification is intended to provide a way to send multiple types of notification messages to django users out of box\n and docs are on the way...\n\nRequirements\n-----\n\n* Python (3.8, 3.9, 3.10)\n* Django (3.1, 3.2, 4.0, 4.1)\n\nWe **highly recommend** and only officially support the latest patch release of\neach Python and Django series.\n\nInstallation\n-----\n\nInstall using `pip`...\n\n    pip install django-user-notification\n\nAdd `\'notification\'` to your `INSTALLED_APPS` setting.\n```python\nINSTALLED_APPS = [\n    ...\n    \'notification\',\n]\n```\n\nQuick Start\n-----\n\nLet\'s take a look at a quick start of using Django user notification to send notification messages to users.\n\nRun the `notification` migrations using:\n\n    python manage.py migrate notification\n\n\nAdd the following to your `settings.py` module:\n\n```python\nINSTALLED_APPS = [\n    ...  # Make sure to include the default installed apps here.\n    \'notification\',\n]\n\nDJANGO_USER_NOTIFICATION = {\n    "aliyunsms": {\n        "access_key_id": "ACCESS_KEY_ID",\n        "access_key_secret": "ACCESS_KEY_SECRET",\n        "sign_name": "SIGN_NAME",\n    },\n    "dingtalkchatbot": {\n        "webhook": "DINGTALK_WEBHOOK",\n    },\n    "dingtalkworkmessage": {\n        "agent_id": "DINGTALK_AGENT_ID",\n        "app_key": "DINGTALK_APP_KEY",\n        "app_secret": "DINGTALK_APP_SECRET",\n    },\n    "dingtalktodotask": {\n        "app_key": "DINGTALK_APP_KEY",\n        "app_secret": "DINGTALK_APP_SECRET",\n    },\n}\n```\n\nLet\'s send a notification\n\n``` {.python}\nfrom django.contrib.auth import get_user_model\nfrom notification.backends import notify_by_email, notify_by_dingtalk_workmessage\n\nUser = get_user_model()\n\nrecipient = User.objects.first()\n\n# send a dingtalk work message notification\nnotify_by_dingtalk_workmessage([recipient], phone_field="phone", title="This is a title", message="A test message")\n\n\n# send a email notiofication\nnotify_by_email([recipient], title="This is a title", message="A test message")\n```\n\nSend Message With Template\n--------------\n\n`django-user-notification` support send notifications with custom template, To\nspecify a custom message template you can provide the `template_code`\nand `context` parameters.\n\n1)  Create a template message with code named `TMP01` on django admin\n\n\n\n2) Provide the `template_code` and `context` to `send` method:\n``` {.python}\n...\n\nnotify_by_email([recipient], template_code="TMP01", context={"content": "Hello"})\n```\n\nSupported backends\n-----------------------------\n\n- `DummyNotificationBackend`: send dummy message\n- `EmailNotificationBackend`: send email notification.\n- `WebsocketNotificationBackend`: send webdocket notification, need `channels` installed\n- `AliyunSMSNotificationBackend`: send aliyun sms notification.\n- `DingTalkChatBotNotificationBackend`: send dingtalk chatbot notification.\n- `DingTalkTODOTaskNotificationBackend`: send dingtalk todo tasks notification\n- `DingTalkWorkMessageNotificationBackend`: send dingtalk work message notification.\n\nRunning the tests\n-----------------\n\nTo run the tests against the current environment:\n\n``` {.bash}\n$ ./manage.py test\n```\n\n### Changelog\n\n0.5.0\n-----\n\n-   Initial release\n\n## Thanks\n\n[![PyCharm](docs/pycharm.svg)](https://www.jetbrains.com/?from=django-user-notification)\n',
    'author': 'Aiden Lu',
    'author_email': 'allaher@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aiden520/django-user-notification',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
