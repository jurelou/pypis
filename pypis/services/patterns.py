import importlib


class SingletonMetaClass(type):
    _instances_ = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances_:
            cls._instances_[cls] = super(SingletonMetaClass, cls).__call__(
                *args, **kwargs
            )
        return cls._instances_[cls]


Singleton = SingletonMetaClass("Singleton", (object,), {})
