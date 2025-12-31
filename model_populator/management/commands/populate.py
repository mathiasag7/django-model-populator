from django.apps import apps
from django.core.management.base import BaseCommand, CommandParser
from model_populator.engine import generate_model_fakes


def get_model_labels(self, options: dict) -> list:
    if model_names := options["models"]:
        app_config = apps.get_app_config(options["apps"][0])
        # Convert model names to lowercase for comparison
        model_names_lower = [name.lower() for name in model_names]
        return [model for model in app_config.get_models() if model._meta.model_name in model_names_lower]
    elif app_labels := options["apps"]:
        model_labels: list = []
        for app_label in app_labels:
            app_config = apps.get_app_config(app_label)
            model_labels.extend([model for model in app_config.get_models()])
        return model_labels
    else:
        return [model for model in apps.get_models()]


class Command(BaseCommand):
    help = "Generate fake data."

    def add_arguments(self, parser: CommandParser) -> None:
        gen_type = parser.add_argument_group("Generation options")
        gen_type.add_argument("apps", type=str, nargs="*", help="App labels to fill with fake data")
        gen_type.add_argument("--all", action="store_true", help="All models will be filled with fake data")

        model_gen_type = gen_type.add_mutually_exclusive_group()
        model_gen_type.add_argument("--models", type=str, nargs="*", help="Model names to fill with fake data")

        parser.add_argument("--num", type=int, help="Number of objects to generate.", default=1)
        parser.add_argument(
            "--m2m", type=int, help="Number of related objects to generate for ManyToManyField.", default=1
        )

    def handle(self, *args, **options) -> None:
        num = options["num"]
        m2m = options["m2m"]

        for model in get_model_labels(self, options):
            generate_model_fakes(model, num_objects=num, m2m_objects_number=m2m)

        self.stdout.write(self.style.SUCCESS("Fake data generated successfully!!!"))
