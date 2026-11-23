from abc import ABC, abstractmethod
import json
import os
from typing import Any
from src.models import Aeroplane


class BaseSaver(ABC):
    """Абстрактный класс для работы с хранилищем данных о самолётах."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет информацию о самолёте в хранилище."""
        pass

    @abstractmethod
    def get_aeroplanes(self, criteria: dict[str, Any] | None = None) -> list[Aeroplane]:
        """Получает список самолётов по заданным критериям."""
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет информацию о самолёте из хранилища."""
        pass


class JSONSaver(BaseSaver):
    """Класс для сохранения и чтения информации о самолётах в JSON-файле."""

    def __init__(self, filename: str = "data/aeroplanes.json") -> None:
        self.__filename = filename
        os.makedirs(os.path.dirname(self.__filename), exist_ok=True)
        if not os.path.exists(self.__filename):
            with open(self.__filename, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def _read_file(self) -> list[dict[str, Any]]:
        """Читает данные из JSON-файла с обработкой исключений."""
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_file(self, data: list[dict[str, Any]]) -> None:
        """Записывает список словарей в JSON-файл."""
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет самолёт в файл, избегая полных дубликатов."""
        data = self._read_file()
        aeroplane_dict = aeroplane.to_dict()
        if aeroplane_dict not in data:
            data.append(aeroplane_dict)
            self._write_file(data)

    def add_aeroplanes(self, aeroplanes: list[Aeroplane]) -> None:
        """Массово сохраняет список самолётов в файл."""
        data = self._read_file()
        for plane in aeroplanes:
            plane_dict = plane.to_dict()
            if plane_dict not in data:
                data.append(plane_dict)
        self._write_file(data)

    def get_aeroplanes(self, criteria: dict[str, Any] | None = None) -> list[Aeroplane]:
        """Возвращает самолёты из файла, соответствующие критериям."""
        data = self._read_file()
        aeroplanes = [Aeroplane.from_dict(item) for item in data]

        if not criteria:
            return aeroplanes

        filtered: list[Aeroplane] = []
        for plane in aeroplanes:
            match = True
            for key, value in criteria.items():
                if getattr(plane, key, None) != value:
                    match = False
                    break
            if match:
                filtered.append(plane)
        return filtered

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет самолёт из JSON-файла."""
        data = self._read_file()
        target = aeroplane.to_dict()
        updated = [item for item in data if item != target]
        self._write_file(updated)
