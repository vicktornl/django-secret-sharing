# Django Secret Sharing

[![Version](https://img.shields.io/pypi/v/djang-secret-sharing.svg?style=flat)](https://pypi.python.org/pypi/django-secret-sharing/)

A secure sharing app for Django.

## Features

* Keep sensitive information out of your chat logs and email via a secure sharing protocal
* REST API
* One time secrets

## Requirements

- Python 3
- Django >= 2

## Installation

Install the package

```
pip install django-secret-sharing
```

Add `django_secret_sharing` to your `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...
    "django_secret_sharing",
]
```

Add the urls

```
urlpatterns = [
  ...
  path("secrets/", include("django_secret_sharing.urls"),),
]
```

Run migrate

```
manage.py migrate
```

## Templates

Override the default templates with your own

**django_secret_sharing/create.html**

```
{% if secret_url %}
    <p>{{ secret_url }}</p>
    <a href="{% url 'django_secret_sharing:create' %}">Create</a>
{% else %}
  <form action="{% url 'django_secret_sharing:create' %}" method="post">
      {% csrf_token %}
      {{ form }}
      <input type="submit" value="Submit">
  </form>
{% endif %}
```

**django_secret_sharing/retrieve.html**

```
<a href="{% url 'django_secret_sharing:view' url_part %}">View</a>
```

**django_secret_sharing/view.html**

```
<textarea disabled>{{ secret }}</textarea>
<a href="{% url 'django_secret_sharing:create' %}">Create</a>
```
