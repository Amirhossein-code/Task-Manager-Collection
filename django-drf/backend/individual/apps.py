from django.apps import AppConfig


class IndividualConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "individual"

    def ready(self):
        import individual.signals
