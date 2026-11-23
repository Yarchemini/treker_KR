from typing import Any


class Aeroplane:
    """Класс для представления информации о самолёте."""

    def __init__(
        self,
        callsign: str | None,
        origin_country: str | None,
        velocity: float | int | None,
        baro_altitude: float | int | None,
        icao24: str = "",
    ) -> None:
        self.__icao24: str = self.__validate_str(icao24, "Неизвестно")
        self.__callsign: str = self.__validate_str(callsign, "Без позывного")
        self.__origin_country: str = self.__validate_str(origin_country, "Неизвестна")
        self.__velocity: float = self.__validate_number(velocity)
        self.__baro_altitude: float = self.__validate_number(baro_altitude)

    @staticmethod
    def __validate_str(value: str | None, default: str) -> str:
        """Валидирует строковые значения и убирает лишние пробелы."""
        if not value or not isinstance(value, str) or not value.strip():
            return default
        return value.strip()

    @staticmethod
    def __validate_number(value: float | int | None) -> float:
        """Валидирует числовые значения (заменяет None или некорректные типы на 0.0)."""
        if value is None or not isinstance(value, (int, float)):
            return 0.0
        return float(value)

    @property
    def icao24(self) -> str:
        return self.__icao24

    @property
    def callsign(self) -> str:
        return self.__callsign

    @property
    def origin_country(self) -> str:
        return self.__origin_country

    @property
    def velocity(self) -> float:
        return self.__velocity

    @property
    def baro_altitude(self) -> float:
        return self.__baro_altitude

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (
            self.__baro_altitude == other.__baro_altitude
            and self.__velocity == other.__velocity
        )

    def __lt__(self, other: object) -> bool:
        """Сравнение самолётов по высоте (при равной высоте — по скорости)."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        if self.__baro_altitude != other.__baro_altitude:
            return self.__baro_altitude < other.__baro_altitude
        return self.__velocity < other.__velocity

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        if self.__baro_altitude != other.__baro_altitude:
            return self.__baro_altitude > other.__baro_altitude
        return self.__velocity > other.__velocity

    def compare_by_velocity(self, other: "Aeroplane") -> int:
        """Явное сравнение по скорости: 1 если быстрее, -1 если медленнее, 0 если равны."""
        if self.__velocity > other.__velocity:
            return 1
        if self.__velocity < other.__velocity:
            return -1
        return 0

    def to_dict(self) -> dict[str, Any]:
        """Преобразует объект в словарь для сохранения в JSON."""
        return {
            "icao24": self.__icao24,
            "callsign": self.__callsign,
            "origin_country": self.__origin_country,
            "velocity": self.__velocity,
            "baro_altitude": self.__baro_altitude,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Aeroplane":
        """Создаёт объект Aeroplane из словаря."""
        return cls(
            callsign=data.get("callsign"),
            origin_country=data.get("origin_country"),
            velocity=data.get("velocity"),
            baro_altitude=data.get("baro_altitude"),
            icao24=data.get("icao24", ""),
        )

    @classmethod
    def cast_to_object_list(cls, states: list[list[Any]]) -> list["Aeroplane"]:
        """Преобразует сырой ответ OpenSky в список объектов Aeroplane."""
        aeroplanes: list[Aeroplane] = []
        for state in states:
            if not isinstance(state, list) or len(state) < 10:
                continue
            aeroplanes.append(
                cls(
                    icao24=state[0],
                    callsign=state[1],
                    origin_country=state[2],
                    baro_altitude=state[7],
                    velocity=state[9],
                )
            )
        return aeroplanes

    def __str__(self) -> str:
        return (
            f"Рейс: {self.__callsign} | Страна: {self.__origin_country} | "
            f"Высота: {self.__baro_altitude} м | Скорость: {self.__velocity} м/с"
        )
