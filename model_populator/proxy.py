from faker.exceptions import UniquenessException

from django.conf import settings


MAX_ATTEMPTS: int = settings.UNIQUE_ATTEMPTS if hasattr(settings, "UNIQUE_ATTEMPTS") else 1000


class SafeUniqueProxy:
    def __init__(self, unique_proxy):
        self._unique = unique_proxy
        self._excluded = {}

    def __getattr__(self, method_name, field_name=None):
        real_method = getattr(self._unique, method_name)

        def wrapper(*args, **kwargs):
            for _ in range(MAX_ATTEMPTS):
                value = real_method(*args, **kwargs)
                if value not in self._excluded.get(field_name, set()):
                    self._unique._seen.setdefault(field_name, set()).add(value)
                    return value
            raise UniquenessException
        return wrapper

    def clear_a_method(self, field_name) -> None:
        self._unique._seen.pop(field_name, None)

    def clear_all(self) -> None:
        self._unique.clear()

    def has_excluded(self, field_name: str) -> bool:
        return bool(self._excluded.get(field_name))

    def exclude(self, field_name: str, values: set) -> None:
        self._excluded.setdefault(field_name, set()).update(values)
    
    def clear_excluded_method(self, field_name: str) -> None:
        self._excluded.pop(field_name, None)
    
    def clear_all_excluded(self) -> None:
        self._excluded.clear()
