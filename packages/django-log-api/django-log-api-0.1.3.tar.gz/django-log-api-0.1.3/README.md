## django-log-api

Allows download django log file via api

### Requirements

- django >= 2.2 
- djangorestframework >= 3.9.2 
- [tailhead](https://github.com/GreatFruitOmsk/tailhead) 

### Installation

1. Install package

```shell
pip install django-log-api

# or
poetry add django-log-api
```

2. Add to the INSTALLED_APPS

settings.py

```python
INSTALLED_APPS = [
    ...,
    "log_api",
]

# log dir path, use Path(), default: BASE_DIR / logs
LOG_API_DIR_PATH = BASE_DIR / "logs"
# log file name, default: 'django.log'
LOG_API_DEFAULT_FILE = "django.log"
# log tail numbers, default: 1000
LOG_API_MAX_READ_LINES = 1000
# log api permission, use drf`s permission, default: AllowAny
LOG_API_PERMISSION_CLASSES = ("rest_framework.permissions.AllowAny",)
```

3. add to urls.py

```python
path(r"logs/", include("log_api.urls")),
```

4. visit 'http://localhost:8000/logs/download/?name=django&tail=100' 

parameters:
- name: log file name
- tail: if null, download entire log file, others the tail lines number