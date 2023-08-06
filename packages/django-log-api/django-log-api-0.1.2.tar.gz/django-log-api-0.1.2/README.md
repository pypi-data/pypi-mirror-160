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
```

3. add to urls.py

```python
path(r"logs/", include("log_api.urls")),
```

4. visit 'http://localhost:8000/logs/download/?name=django&tail=100' 

parameters:
- name: log file name
- tail: if null, download entire log file, others the tail lines number