from src.api import AeroplanesAPI
from src.models import Aeroplane
from src.storage import JSONSaver
from src.utils import (
    filter_aeroplanes,
    get_aeroplanes_by_altitude,
    get_top_aeroplanes,
    print_aeroplanes,
    sort_aeroplanes,
)


def user_interaction() -> None:
    """Функция взаимодействия с пользователем через консоль."""
    api = AeroplanesAPI()
    saver = JSONSaver()

    country = input("Введите название страны (например, Spain или Russia): ").strip()
    if not country:
        print("Название страны не может быть пустым.")
        return

    print(f"Загружаем данные о самолётах над страной {country}...")
    raw_states = api.get_aeroplanes(country)
    if not raw_states:
        print("Не удалось получить данные о самолётах или воздушное пространство пусто.")
        return

    aeroplanes = Aeroplane.cast_to_object_list(raw_states)
    saver.add_aeroplanes(aeroplanes)
    print(f"Загружено и сохранено в JSON: {len(aeroplanes)} самолётов.")

    try:
        top_n_input = input("Введите количество самолётов для вывода в топ N: ").strip()
        top_n = int(top_n_input)
        if top_n <= 0:
            raise ValueError
    except ValueError:
        print("Некорректное число, будет выведено топ 5 самолётов.")
        top_n = 5

    filter_words = input(
        "Введите страны регистрации для фильтрации через пробел (или Enter, чтобы пропустить): "
    ).split()
    altitude_range = input(
        "Введите диапазон высот в метрах (пример: 5000 - 12000, или Enter, чтобы пропустить): "
    )

    filtered = filter_aeroplanes(aeroplanes, filter_words)
    ranged = get_aeroplanes_by_altitude(filtered, altitude_range)
    sorted_planes = sort_aeroplanes(ranged)
    top_planes = get_top_aeroplanes(sorted_planes, top_n)

    print_aeroplanes(top_planes)


if __name__ == "__main__":
    user_interaction()
