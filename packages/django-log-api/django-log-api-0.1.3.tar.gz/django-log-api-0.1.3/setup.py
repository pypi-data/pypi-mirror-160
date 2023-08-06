# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['log_api']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2', 'djangorestframework>=3.9.2', 'tailhead>=1.0.2']

setup_kwargs = {
    'name': 'django-log-api',
    'version': '0.1.3',
    'description': 'Allows download django log file via api',
    'long_description': '## django-log-api\n\nAllows download django log file via api\n\n### Requirements\n\n- django >= 2.2 \n- djangorestframework >= 3.9.2 \n- [tailhead](https://github.com/GreatFruitOmsk/tailhead) \n\n### Installation\n\n1. Install package\n\n```shell\npip install django-log-api\n\n# or\npoetry add django-log-api\n```\n\n2. Add to the INSTALLED_APPS\n\nsettings.py\n\n```python\nINSTALLED_APPS = [\n    ...,\n    "log_api",\n]\n\n# log dir path, use Path(), default: BASE_DIR / logs\nLOG_API_DIR_PATH = BASE_DIR / "logs"\n# log file name, default: \'django.log\'\nLOG_API_DEFAULT_FILE = "django.log"\n# log tail numbers, default: 1000\nLOG_API_MAX_READ_LINES = 1000\n# log api permission, use drf`s permission, default: AllowAny\nLOG_API_PERMISSION_CLASSES = ("rest_framework.permissions.AllowAny",)\n```\n\n3. add to urls.py\n\n```python\npath(r"logs/", include("log_api.urls")),\n```\n\n4. visit \'http://localhost:8000/logs/download/?name=django&tail=100\' \n\nparameters:\n- name: log file name\n- tail: if null, download entire log file, others the tail lines number',
    'author': 'luocy',
    'author_email': 'luocy77@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/django-log-api',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
