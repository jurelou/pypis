from dynaconf import settings, Validator


validators = [
    #Common validators
    Validator("APP_NAME", "LOG_FILE", must_exist=True,is_type_of=str),
    Validator("LOG_LEVEL", is_in=("info", "debug"), must_exist=True),

    #Fastapi validators
    Validator("FASTAPI.DEBUG", must_exist=True, is_type_of=bool),
    Validator("FASTAPI.API_PREFIX", must_exist=True,is_type_of=str),

    #Database validators
    Validator("DATABASE.URL", must_exist=True,is_type_of=str),
    Validator("DATABASE.MIN_CONNECTIONS_COUNT", must_exist=True, is_type_of=int, gt=0),
    Validator("DATABASE.MAX_CONNECTIONS_COUNT", must_exist=True, is_type_of=int, gte=settings.DATABASE.MIN_CONNECTIONS_COUNT),

]


settings.validators.register(*validators)


def validate_settings():
    settings.validators.validate()
