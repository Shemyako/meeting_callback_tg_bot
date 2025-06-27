from typing import Any

from .exceptions import ConfigurationError
from .google_client import GoogleClient


class ConferenceCache:
    _config_cache: set[str] = set()

    @classmethod
    def get_config(cls) -> set[str]:
        return cls._config_cache

    @classmethod
    async def __prepare_data(cls, data: list[list[Any]]) -> list[str]:
        return [row[0].strip() for row in data if row and row[0]]

    @classmethod
    async def refresh_config(cls) -> None:
        data = await GoogleClient().get_tab_data("config")

        data_to_update = await cls.__prepare_data(data)

        if data_to_update:
            cls._config_cache.clear()
            cls._config_cache.update(data_to_update)
        else:
            raise ConfigurationError("Ошбика конфигурации. Свяжитесь с администратором")
