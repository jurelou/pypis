from dynaconf import Validator, settings

validators = [
    # Common validators
    Validator("APP_NAME", must_exist=True, is_type_of=str),
    # Logs validators
    Validator("LOGS.FILE", must_exist=True, is_type_of=str),
    Validator("LOGS.LEVEL", is_in=("info", "debug"), must_exist=True),
    # Fastapi validators
    Validator("FASTAPI.DEBUG", must_exist=True, is_type_of=bool),
    Validator("FASTAPI.API_PREFIX", must_exist=True, is_type_of=str),
    # Database validators
    Validator("DATABASE.URL", must_exist=True, is_type_of=str),
    Validator("DATABASE.MIN_CONNECTIONS_COUNT", must_exist=True, is_type_of=int, gt=0),
    Validator(
        "DATABASE.MAX_CONNECTIONS_COUNT",
        must_exist=True,
        is_type_of=int,
        gte=settings.DATABASE.MIN_CONNECTIONS_COUNT,
    ),
    # Packages validator
    Validator("PACKAGES.BASE_DIRECTORY", must_exist=True, is_type_of=str),
    Validator("PACKAGES.MAX_PACKAGES_VERSION_CACHE", must_exist=True, is_type_of=int, gt=0),
    #Pypi proxy validator
    Validator("PYPI_PROXY.TIMEOUT", must_exist=True, is_type_of=int, gt=1),
]


settings.validators.register(*validators)


def validate_settings():
    settings.validators.validate()
