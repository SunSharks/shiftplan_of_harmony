from django.apps import AppConfig


class SolsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sols'

    def ready(self):
        import sols.signals 

