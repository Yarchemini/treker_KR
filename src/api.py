from abc import ABC, abstractmethod
from typing import Any
import requests


class BaseAPI(ABC):
    """Абстрактный класс для работы с внешними API."""

    @abstractmethod
    def _connect(self, url: str, params: dict[str, Any] | None = None) -> Any:
        """Приватный метод подключения к API."""
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> list[list[Any]]:
        """Получение данных о самолётах в воздушном пространстве страны."""
        pass


class AeroplanesAPI(BaseAPI):
    """Класс для получения координат страны (Nominatim) и данных о самолётах (OpenSky)."""

    def __init__(self) -> None:
        self.__nominatim_url = "https://nominatim." + "openstreetmap.org/search"
        self.__opensky_url = "https://opensky-network.org" + "/api/states/all"
        self.__headers = {"User-Agent": "AeroplaneTrackerStudentProject/1.0"}

    def _connect(self, url: str, params: dict[str, Any] | None = None) -> Any:
        """Отправляет GET-запрос и возвращает распарсенный JSON."""
        try:
            response = requests.get(
                url, params=params, headers=self.__headers, timeout=15
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка при обращении к API ({url}): {e}")
            return None

    def _get_country_bounds(self, country: str) -> dict[str, float] | None:
        """Получает координаты boundingbox для указанной страны."""
        params = {"q": country, "format": "json", "limit": 1}
        data = self._connect(self.__nominatim_url, params=params)

        if not data or not isinstance(data, list):
            print(f"Страна '{country}' не найдена.")
            return None

        bbox = data[0].get("boundingbox")
        if not bbox or len(bbox) < 4:
            return None

        # Nominatim возвращает [south_lat, north_lat, west_lon, east_lon]
        return {
            "lamin": float(bbox[0]),
            "lamax": float(bbox[1]),
            "lomin": float(bbox[2]),
            "lomax": float(bbox[3]),
        }

    def get_aeroplanes(self, country: str) -> list[list[Any]]:
        """Возвращает список векторов состояния самолётов в границах страны."""
        bounds = self._get_country_bounds(country)
        if not bounds:
            return []

        data = self._connect(self.__opensky_url, params=bounds)
        if not data or "states" not in data or data["states"] is None:
            return []

        return data["states"]
