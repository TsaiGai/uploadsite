from django.apps import AppConfig


# creates a new app for the site
class UploadappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'uploadapp'
