from django.apps import AppConfig


class IndividualConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "individual"

    # Required for the signals to work
    def ready(self):
        import individual.signals
