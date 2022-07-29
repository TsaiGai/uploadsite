from django.apps import AppConfig

# creates an app for the home page
class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
