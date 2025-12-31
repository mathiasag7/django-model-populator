import random
from faker import Faker
from typing import TypeVar
from collections import defaultdict
from tqdm import tqdm, trange

from django.apps import apps
from django.utils.translation import get_language
from django.contrib.auth.hashers import make_password
from django.db import models

from model_populator.proxy import SafeUniqueProxy
from model_populator.field_mappings import (
    update_settings,
    FIELD_NAME_MAPPING,
    FIELD_TYPE_MAPPING,
    EXCLUDED_APPS,
    EXCLUDED_MODELS,
    AUTO_CREATE_RELATED_MODELS,
)


T = TypeVar("T")

_OBJECT_CREATED_COUNT: dict = defaultdict(int)
_fake: Faker = Faker(locale=get_language())
_fake_unique: SafeUniqueProxy = SafeUniqueProxy(_fake.unique)


def _get_fake_value_based_on_type(fake, mapping):
    return getattr(fake, mapping[0]["faker"])()


def _get_fake_decimal_value(fake, mapping):
    return getattr(fake, mapping[0]["faker"])(
        left_digits=mapping[0].get("left_digits", 2),
        right_digits=mapping[0].get("right_digits", 2),
        positive=mapping[0].get("positive", True),
    )


def _get_fake_char_value(fake, mapping, field) -> str:
    if field.choices:
        return random.choice(field.choices)[0]
    else:
        for provider, patterns in FIELD_NAME_MAPPING.items():
            if field.name in patterns:
                if provider == "password":
                    return make_password(getattr(fake, provider)())
                return getattr(fake, provider)()

        min_length = getattr(field, "min_length", None)
        max_length = getattr(field, "max_length", None)
        for el in mapping:
            if el.get("max_length") is not None:
                if min_length is not None:
                    if min_length > el["max_length"]:
                        continue
                    return getattr(fake, el["faker"])()

                elif max_length is not None:
                    if el["max_length"] > max_length:
                        continue
                    return getattr(fake, el["faker"])()
    return fake.sentence(nb_words=5, variable_nb_words=True)


def _set_m2m_objects(object, fields: tuple, m2m_objects_number: int = 1) -> None:
    """
    Sets ManyToManyField objects for a given model instance.

    :param object: The model instance to set ManyToManyField objects for.
    :param fields: List of fields to process, assumed to be ManyToManyFields.
    :param m2m_objects_number: Number of related objects to assign, defaults to 1.
    :return: None
    """

    for field in fields:
        object_m2m = getattr(object, field.name)
        field_model = field.related_model
        if AUTO_CREATE_RELATED_MODELS:
            generate_fake_data(field_model, num_objects=m2m_objects_number)
        object_m2m.set([random.choice(field_model.objects.all()) for _ in range(m2m_objects_number)])


def _get_fake_fk_object(field, num_objects: int = 1):
    """
    Returns a random related object for a ForeignKey or OneToOneField.
    """
    model = field.related_model
    if AUTO_CREATE_RELATED_MODELS:
        generate_fake_data(model, num_objects=num_objects)
    return random.choice(model.objects.all())


def generate_fake_data(model, fields: list = [], num_objects: int = 1, m2m_related_objects_number: int = 1):
    """
    Fills a specific model with fake data.

    :param model: Model class to fill with fake data.
    :param fields: List of fields to fill, if empty all fields will be filled.
    :param num_objects: Number of objects to generate.
    :param m2m_related_objects_number: Number of related objects to generate for ManyToManyField.
    :return: None
    :raises: ValueError if the model is not registered in Django.
    :raises: TypeError if the model is not a Django model.
    :raises: Exception if an error occurs while generating fake data.
    :example:
        from my_app.models import MyModel
        generate_fake_data(MyModel, fields=['name', 'description'], num_objects=10)
    :note: This function will not fill models from excluded apps.
    :note: If the model has a ForeignKey or OneToOneField, it will
           attempt to assign a random related object from the related model.
    :note: If the model has a ManyToManyField, it will not fill it
           as it requires a different approach to handle multiple related objects.
    :note: If the model has a field that is not in the FIELD_TYPE_MAPPING,
           it will skip that field.
    :note: If the model has a field that is not editable or auto-created,
           it will skip that field.

    """

    global _fake
    global _fake_unique
    object = model()
    _fields: list = fields or [
        f
        for f in model._meta.get_fields()
        if f.editable and not f.auto_created and not isinstance(f, models.ManyToManyField)
    ]

    if model_unique_together := model._meta.unique_together:
        _fake_unique.exclude(model_unique_together, model.objects.values_list(*model_unique_together[0]))

    for field in _fields:

        field_type = field.__class__.__name__
        mapping = FIELD_TYPE_MAPPING.get(field_type, [])

        fake: SafeUniqueProxy | Faker = _fake_unique if field.unique else _fake
        if field.unique and not fake.has_excluded(field.attname):
            fake.exclude(field.attname, model.objects.values_list(field.attname, flat=True))

        if field.one_to_one:
            value = generate_fake_data(field.related_model)
        elif field.many_to_one:
            value = _get_fake_fk_object(field, num_objects)
        else:
            if field_type == "CharField":
                fake_value = _get_fake_char_value(fake, mapping, field)
            elif field_type == "DecimalField":
                fake_value = _get_fake_decimal_value(fake, mapping)
            else:
                fake_value = _get_fake_value_based_on_type(fake, mapping)

            try:
                value = field.get_prep_value(fake_value)
            except ValueError:
                if field.has_default():
                    value = field.default()
                else:
                    if field.blank and field.null:
                        value = None
                    else:
                        continue

        setattr(object, field.name, value)
    object.save()
    _OBJECT_CREATED_COUNT[model._meta.model_name] += 1

    if many_to_many_fields := object.__class__._meta.many_to_many:
        m2m_related_objects_number = min(m2m_related_objects_number, num_objects)
        _set_m2m_objects(object, many_to_many_fields, m2m_related_objects_number)

    return object


def get_model_description(model) -> str:
    return f"{model._meta.model_name.capitalize()}[{model._meta.app_label}]"


def generate_all_fakes(
    fields: list = [], num_objects: int = 1, m2m_objects_number: int = 1, output: bool = True
) -> None:
    """
    Fills all models with fake data.

    :param fields: List of fields to fill, if empty all fields will be filled.
    :param num_objects: Number of objects to generate for each model.
    :param m2m_objects_number: Number of related objects to generate for ManyToManyField.
    :return: True if successful, False otherwise.
    """

    for model in apps.get_models():
        generate_model_fakes(model, fields, num_objects, m2m_objects_number)
    if output:
        print("All models have been filled with fake data.")


def generate_app_fakes(
    app_label: str, fields: list = [], num_objects: int = 1, m2m_objects_number: int = 1, output: bool = True
) -> None:
    """
    Fills all models in a specific app with fake data.

    :param app_label: App label to fill with fake data.
    :param fields: List of fields to fill, if empty all fields will be filled.
    :param num_objects: Number of objects to generate for each model.
    :param m2m_objects_number: Number of related objects to generate for ManyToManyField.
    :return: True if successful, False otherwise.
    """

    for model in apps.get_app_config(app_label).get_models():
        generate_model_fakes(model, fields, num_objects, m2m_objects_number)
    if output:
        print(f"All models in app '{app_label}' have been filled with fake data.")


def generate_model_fakes(model, fields: list = [], num_objects: int = 1, m2m_objects_number: int = 1) -> None:
    """
    Fills a specific model with fake data.

    :param model_name: Model name to fill with fake data.
    :param fields: List of fields to fill, if empty all fields will be filled.
    :param num_objects: Number of objects to generate.
    :param m2m_objects_number: Number of related objects to generate for ManyToManyField.
    :return: True if successful, False otherwise.
    """

    if model._meta.app_label in EXCLUDED_APPS or model in EXCLUDED_MODELS:
        return
    if _OBJECT_CREATED_COUNT[model._meta.model_name] >= num_objects:
        return

    for _ in trange(num_objects, desc=get_model_description(model)):
        generate_fake_data(model, fields, num_objects, m2m_objects_number)


def generate_fakes_by_name(
    model_name: str, app_label: str, fields: list = [], num_objects: int = 1, m2m_objects_number: int = 1
) -> None:
    """
    Fills a specific model in a given app with fake data.

    :param app_label: The label of the app containing the model.
    :param model_name: The name of the model to fill with fake data.
    :param fields: List of fields to fill, if empty all fields will be filled.
    :param num_objects: Number of objects to generate.
    :param m2m_objects_number: Number of related objects to generate for ManyToManyField.
    :return: None
    :raises: LookupError if the model is not found.
    """

    try:
        model = apps.get_model(app_label, model_name)
        generate_model_fakes(model, fields, num_objects, m2m_objects_number)
    except LookupError:
        print(f"Model '{model_name}' not found.")
        return
