from django.conf import settings


EXCLUDED_APPS: list = ["sessions", "admin"]

EXCLUDED_MODELS: list = ["Session", "Permission", "ContentType", "Site", "LogEntry"]


AUTO_CREATE_RELATED_MODELS: bool = settings.AUTO_CREATE_RELATED_MODELS if hasattr(settings, "AUTO_CREATE_RELATED_MODELS") else True


FIELD_TYPES: dict = {
    "uuid": [
        "UUIDField",
    ],
    "json": [
        "JSONField",
    ],
    "float": ["FloatField", "DecimalField"],
    "string": ["CharField", "TextField", "SlugField", "EmailField", "URLField", "GenericIPAddressField"],
    "integer": [
        "IntegerField",
        "BigIntegerField",
        "PositiveSmallIntegerField",
        "PositiveBigIntegerField",
        "SmallIntegerField",
        "PositiveIntegerField",
    ],
    "date": ["DateField", "DateTimeField", "TimeField", "DurationField"],
    "boolean": ["BooleanField", "NullBooleanField"],
    "autofield": ["AutoField", "BigAutoField", "SmallAutoField"],
    "file": ["FileField", "FilePathField", "ImageField", "FieldFile"],
}


FIELD_TYPE_MAPPING: dict = {
    "CharField": [
        {"faker": "word", "max_length": 15},
        {"faker": "sentence", "max_length": 50},
        {"faker": "paragraph", "max_length": None},
    ],
    "TextField": [
        {"faker": "paragraph"},
        {"faker": "text"},
    ],
    "SlugField": [
        {"faker": "slug"},
    ],
    "EmailField": [
        {"faker": "email"},
    ],
    "URLField": [
        {"faker": "url"},
    ],
    "GenericIPAddressField": [
        {"faker": "ipv4"},
        {"faker": "ipv6"},
    ],
    "JSONField": [
        {"faker": "json"},
    ],
    "UUIDField": [
        {"faker": "uuid4"},
    ],
    "IntegerField": [
        {"faker": "random_int"},
    ],
    "PositiveIntegerField": [
        {"faker": "random_int", "min": 0},
    ],
    "PositiveSmallIntegerField": [
        {"faker": "random_int", "min": 0, "max": 32767},
    ],
    "SmallIntegerField": [
        {"faker": "random_int", "min": -32768, "max": 32767},
    ],
    "BigIntegerField": [
        {"faker": "random_int"},
    ],
    "FloatField": [
        {"faker": "random_float"},
    ],
    "DecimalField": [
        {"faker": "pydecimal", "left_digits": 2, "right_digits": 2, "positive": True},
    ],
    "DateField": [
        {"faker": "date"},
    ],
    "DateTimeField": [
        {"faker": "date_time"},
    ],
    "TimeField": [
        {"faker": "time"},
    ],
    "DurationField": [
        {"faker": "time_delta"},
    ],
    "BooleanField": [
        {"faker": "boolean"},
    ],
    "NullBooleanField": [
        {"faker": "boolean"},
    ],
    "BinaryField": [
        {"faker": "binary"},
    ],
    "IPAddressField": [
        {"faker": "ipv4"},
        {"faker": "ipv6"},
    ],
    "FilePathField": [
        {"faker": "file_path"},
    ],
    "ImageField": [
        {"faker": "image_url"},
    ],
    "FileField": [
        {"faker": "file_path"},
    ],
    "AutoField": [
        {"faker": "auto_field"},
    ],
    "BigAutoField": [
        {"faker": "big_auto_field"},
    ],
    "SmallAutoField": [
        {"faker": "small_auto_field"},
    ],
    "FieldFile": [
        {"faker": "field_file"},
    ],
}


FIELD_NAME_MAPPING: dict = {
    "name": ["name", "full_name", "person", "contact_name", "display_name", "nom_complet"],
    "first_name": ["first_name", "fname", "prenom", "user_first_name"],
    "last_name": ["last_name", "lname", "surname", "nom", "user_last_name"],
    "email": ["email", "user_email", "contact_email", "mail", "email_address"],
    "phone_number": ["phone", "phone_number", "tel", "telephone", "mobile", "contact_phone"],
    "company": ["company", "company_name", "employer", "business", "organisation", "startup_name", "entreprise"],
    "job": ["job", "job_title", "occupation", "position", "profession"],
    "address": ["address", "full_address", "residence", "home_address"],
    "street_address": ["street", "street_address", "rue"],
    "city": ["city", "ville", "town"],
    "state": ["state", "province", "region"],
    "country": ["country", "nation", "pays"],
    "postcode": ["zip", "postal_code", "postcode", "code_postal"],
    "url": ["url", "website", "site", "webpage", "page_url"],
    "slug": ["slug", "url_slug", "shortlink"],
    "user_name": ["username", "login", "user_name", "pseudo", "handle"],
    "password": ["password", "passcode", "mot_de_passe"],
    "uuid4": ["uuid", "uuid4", "unique_id", "external_id", "identifier"],
    "iban": ["iban", "bank_account", "compte_bancaire"],
    "isbn13": ["sbn", "isbn", "isbn_13", "isbn_10"],
    "swift": ["swift", "bic", "bank_swift"],
    "color_name": ["color", "couleur", "theme_color"],
    "language_name": ["language", "lang", "langue", "locale"],
    "currency_code": ["currency", "devise", "currency_code"],
    "file_name": ["filename", "file", "document_name"],
    "ipv4": ["ip", "ipv4", "ip_address"],
    "mac_address": ["mac", "mac_address"],
    "domain_name": ["domain", "domain_name", "host"],
    "paragraph": ["bio", "description", "about", "summary", "profile", "content"],
    "sentence": ["title", "headline", "caption", "subject", "status", "message"],
    "word": ["tag", "label", "category", "type", "code", "kind"],
    "text": ["note", "comment", "details", "instructions", "remarks", "feedback"],
    "image_url": ["image", "image_url", "profile_pic", "avatar", "thumbnail", "cover_photo", "photo", "img"],
    "image": ["image_file", "image_path", "img_file", "uploaded_image", "photo_file"],
    "file_name": ["file", "filename", "document_name", "upload_file", "report_name", "csv_name"],
    "file_path": ["file_path", "document_path", "upload_path", "doc_path", "attachment_path"],
    "mime_type": ["mime", "mime_type", "content_type", "media_type"],
    "password": ["password", "passcode", "mot_de_passe"],
}


def update_settings() -> None:
    if hasattr(settings, "FK_EXCLUDED_APPS"):
        EXCLUDED_APPS = settings.FK_EXCLUDED_APPS
    if hasattr(settings, "FK_EXCLUDED_MODELS"):
        EXCLUDED_MODELS = settings.FK_EXCLUDED_MODELS
    if hasattr(settings, "FK_EXTRA_EXCLUDED_APPS"):
        EXCLUDED_APPS += settings.FK_EXTRA_EXCLUDED_APPS
    if hasattr(settings, "FK_EXTRA_EXCLUDED_MODELS"):
        EXCLUDED_MODELS += settings.FK_EXTRA_EXCLUDED_MODELS
    if hasattr(settings, "FK_EXTRA_FIELD_TYPES"):
        FIELD_TYPES.update(settings.FK_EXTRA_FIELD_TYPES)
    if hasattr(settings, "FK_EXTRA_FIELD_TYPE_MAPPING"):
        FIELD_TYPE_MAPPING.update(settings.FK_EXTRA_FIELD_TYPE_MAPPING)
    if hasattr(settings, "FK_EXTRA_FIELD_NAME_MAPPING"):
        FIELD_NAME_MAPPING.update(settings.FK_EXTRA_FIELD_NAME_MAPPING)
