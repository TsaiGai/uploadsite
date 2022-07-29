from django.apps import AppConfig


# creates a new app for the site
class ForecastConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forecast'
