from src.models import Aeroplane


def filter_aeroplanes(
    aeroplanes: list[Aeroplane], filter_words: list[str]
) -> list[Aeroplane]:
    """Фильтрует самолёты по списку стран регистрации (без учёта регистра)."""
    if not filter_words:
        return aeroplanes
    normalized = [word.strip().lower() for word in filter_words if word.strip()]
    return [
        plane
        for plane in aeroplanes
        if any(word in plane.origin_country.lower() for word in normalized)
    ]


def get_aeroplanes_by_altitude(
    aeroplanes: list[Aeroplane], altitude_range: str
) -> list[Aeroplane]:
    """Фильтрует самолёты по диапазону высот формата '1000 - 12000'."""
    if not altitude_range.strip():
        return aeroplanes

    try:
        parts = altitude_range.replace(" ", "").split("-")
        if len(parts) != 2:
            raise ValueError("Некорректный формат диапазона.")
        min_alt, max_alt = float(parts[0]), float(parts[1])
        if min_alt > max_alt:
            min_alt, max_alt = max_alt, min_alt
    except ValueError:
        print("Некорректный диапазон высот (ожидается формат 'min - max'). Фильтр пропущен.")
        return aeroplanes

    return [
        plane
        for plane in aeroplanes
        if min_alt <= plane.baro_altitude <= max_alt
    ]


def sort_aeroplanes(aeroplanes: list[Aeroplane]) -> list[Aeroplane]:
    """Сортирует самолёты по убыванию высоты (DESC)."""
    return sorted(aeroplanes, reverse=True)


def get_top_aeroplanes(aeroplanes: list[Aeroplane], top_n: int) -> list[Aeroplane]:
    """Возвращает топ N самолётов."""
    if top_n <= 0:
        return []
    return aeroplanes[:top_n]


def print_aeroplanes(aeroplanes: list[Aeroplane]) -> None:
    """Выводит список самолётов в человекочитаемом виде."""
    if not aeroplanes:
        print("\nСамолёты по заданным критериям не найдены.")
        return

    print(f"\nНайдено самолётов: {len(aeroplanes)}")
    print("-" * 75)
    for idx, plane in enumerate(aeroplanes, start=1):
        print(f"{idx}. {plane}")
    print("-" * 75)
