# Django Secret Sharing

[![Version](https://img.shields.io/pypi/v/django-secret-sharing.svg?style=flat)](https://pypi.python.org/pypi/django-secret-sharing/)
![CI](https://github.com/vicktornl/django-secret-sharing/actions/workflows/ci.yml/badge.svg)


A secure sharing app for Django.

## Features

* Keep sensitive information out of your chat logs and email via a secure sharing protocol
* REST API
* One time secrets
* Expiry dates
* Create random passwords
* Secure S3 presigned file transfers

## Requirements

- Python 3
- Django >= 2

## Installation

Install the package

```
pip install django-secret-sharing
```

If you use file trasfers with AWS S3, install the package with `pip install django-secret-sharing[aws]`.

Add `django_secret_sharing` to your `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...
    "django_secret_sharing",
]
```

Add the urls (`api_urls` not needed when you don't use file transfers or any other API features)

```
urlpatterns = [
  ...
  path("secrets/", include("django_secret_sharing.urls"),),
  path("api/secrets/", include("django_secret_sharing.api_urls"),),
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
      <a href="{% url 'django_secret_sharing:generate-password' %}">Generate password</a>
  </form>
{% endif %}

{% block scripts %}
{% include "django_secret_sharing/file_transfer_simple.html" %}
{% include "django_secret_sharing/file_transfer_scripts.html" %}
{% endblock %}
```

**django_secret_sharing/retrieve.html**

```
<a href="{% url 'django_secret_sharing:view' url_part %}">View</a>
```

**django_secret_sharing/view.html**

```
<textarea disabled>{{ value }}</textarea>
{% if secret.files.all %}
<ul>
    {% for file in secret.files.all %}
    <li>
        <a href="{{ file.download_url }}" target="_blank" ref="noopener noreferrer">{{ file.filename }}</a>
    </li>
    {% endfor %}
</ul>
{% endif %}
<a href="{% url 'django_secret_sharing:create' %}">Create</a>
```

## File transfers

File transfers are supported out of the box in this app.

Key is the value of the hidden input `file_refs`. If any file should be send along with the sercret to be created, make sure it's uploaded via a secure upload url (retrieved via the API). The uploaded file ref (commonly the path to the uploaded file) should be appended to the `file_refs` value (comma-separated for multiple files).

Important to know is that the upload path is generated via the backend and it's unique. This way we prevent the user can overwrite/see files, in any way, from other users.

Make sure before submitting the form the files are uploaded (e.g. show a user friendly progress bar during this process).

In order to provide a interface for uploading files and put the value in the `file_refs` input JavaScript is needed. As this implementation is very client specific, it's up to to build that part of the code. Although, for the very minimalistic implementation (and example), we offer a default JavaScript implementation; see `django_secret_sharing/file_transfer_simple.html`. We do recommend build your own with e.g. a proper drag & drop interface.

You can also only include the `uploadFile` JavaScript method by including `django_secret_sharing/file_transfer_scripts.html` into your template and use it with your bespoke JavaScript implementation.

Note: make sure your AWS S3 bucket is set to private and CORS permissions are setup correctly (advice is to keep the rules as strict as possible for best security measurements).

### file_transfer_scripts.html

`window.handleSecretFileUploaded`

This method can optionally be defined in your JavaScript in order to handle successfull file upload (tip: use it for setting the `file_refs` value).

Example:

```javascript
const fileRefsInput = document.getElementById('id_file_refs');

window.handleSecretFileUploaded = (fileRef, file) => {
  fileRefsInput.value = fileRefsInput.value.split(",").concat(fileRef).join(",")
};
```

## Commands

### delete_expired_files

Deletes expired and unfinished files. It's recommended to run this command at least once a day in order to minimize storage limitations (or increase costs optimizations).

## Troubleshooting

###### botocore.exceptions.ClientError: An error occurred (400) when calling the HeadObject operation: Bad Request

Add the `AWS_DEFAULT_REGION` environment variable, e.g. with `eu-west-1`.

###### My files are publicly available in AWS S3

Bad thing! Make sure your bucket permissions are set to private (default).
