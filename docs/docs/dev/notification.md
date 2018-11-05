# Nofification

## Email Settings of Django
Settins are in `app/settings.py`. For more detail, see [here](https://docs.djangoproject.com/ja/2.0/topics/email/).



#### For development

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

#### For production mode

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'apptest'
EMAIL_HOST_PASSWORD = 'xxxxxxxx'
EMAIL_USE_TLS = False
```



!!! Info
	For development, EMAIL_BACKEND is set to `django.core.mail.backends.console.EmailBackend`. If you want to send acutual Email, please modifi `app/settings.py` as above.
