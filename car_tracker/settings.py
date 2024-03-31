import os
from dataclasses import dataclass, Field, fields, MISSING
from distutils.util import strtobool


def _cast_dataclass_type(field: Field, value: str):
    """
    Переводит значение из строки в тип поля dataclass.
    """
    if field.type is bool:
        return bool(strtobool(value))
    return field.type(value)


def _is_dataclass_field_have_default(field: Field):
    return field.default is not MISSING or field.default_factory is not MISSING


@dataclass(kw_only=True)
class Settings:
    def __post_init__(self):
        self.MINIO_SECURE = True if 'https' in self.MINIO_URL else False

    # General settings
    SENTRY_DSN: str = ''

    # MINIO
    MINIO_URL: str = 'http://127.0.0.1:9000'
    MINIO_ACCESS_KEY: str = ('access_key',)
    MINIO_SECRET_KEY: str = 'secret_key'
    MINIO_BUCKET_NAME: str = 'cars'
    MINIO_SECURE: bool = False

    # NATS
    NATS_URL: str = 'nats://localhost:4222'
    # Куда класть урл на картинку с минио
    DETECTED_CAR_STREAM_NAME: str = 'detected_cars'

    DEBUG: bool = False

    @classmethod
    def from_env(cls):
        """
        Берет настройки из переменных окружения.

        В случа если настройка не задана вызовется исключение `ValueError`.
        """
        settings_fields = fields(cls)
        kwargs = {}
        for setting_field in settings_fields:
            env_value = os.getenv(setting_field.name)

            if env_value is not None:
                kwargs[setting_field.name] = _cast_dataclass_type(setting_field, env_value)
            elif not _is_dataclass_field_have_default(setting_field):
                raise ValueError(f'Не задана настройка для {setting_field.name}.')

        return cls(**kwargs)

    @classmethod
    def from_env_file(cls, file_name: str = '.env'):
        """
        Загружает настройки из енв файла.
        """
        from dotenv import load_dotenv

        load_dotenv(file_name)
        return cls.from_env()


settings = Settings.from_env_file()
