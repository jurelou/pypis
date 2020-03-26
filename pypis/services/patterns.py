from typing import Dict


class SingletonMetaClass(type):
    _instances_: Dict[type, type] = {}

    def __call__(cls, *args, **kwargs):  # type: ignore
        """Singleton metaclass."""
        if cls not in cls._instances_:
            cls._instances_[cls] = super(SingletonMetaClass, cls).__call__(
                *args, **kwargs
            )
        return cls._instances_[cls]


Singleton = SingletonMetaClass("Singleton", (object,), {})
