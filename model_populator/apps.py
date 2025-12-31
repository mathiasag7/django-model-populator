from django.apps import AppConfig


class ModelPopulatorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "model_populator"

    def ready(self):
        from model_populator.field_mappings import update_settings

        update_settings()
