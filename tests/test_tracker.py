from unittest.mock import patch
from src.api import AeroplanesAPI
from src.models import Aeroplane
from src.storage import JSONSaver
from src.utils import (
    filter_aeroplanes,
    get_aeroplanes_by_altitude,
    get_top_aeroplanes,
    sort_aeroplanes,
)


def test_aeroplane_validation_and_comparison() -> None:
    p1 = Aeroplane(" UAL123 ", "United States", 250.5, 10000.0, "a1b2c3")
    p2 = Aeroplane(None, None, None, 12000.0, "d4e5f6")

    assert p1.callsign == "UAL123"
    assert p2.callsign == "Без позывного"
    assert p2.origin_country == "Неизвестна"
    assert p2.velocity == 0.0
    assert p2 > p1
    assert p1 < p2
    assert p1.compare_by_velocity(p2) == 1


def test_cast_to_object_list() -> None:
    raw = [
        ["abc123", "AFL001  ", "Russia", 0, 0, 37.5, 55.7, 9500.0, False, 230.0],
        ["invalid_row"],
    ]
    planes = Aeroplane.cast_to_object_list(raw)
    assert len(planes) == 1
    assert planes[0].callsign == "AFL001"
    assert planes[0].baro_altitude == 9500.0


def test_utils_functions() -> None:
    planes = [
        Aeroplane("P1", "Spain", 200, 5000),
        Aeroplane("P2", "Germany", 250, 11000),
        Aeroplane("P3", "Spain", 220, 8000),
    ]
    filtered = filter_aeroplanes(planes, ["spain"])
    assert len(filtered) == 2

    ranged = get_aeroplanes_by_altitude(filtered, "6000 - 10000")
    assert len(ranged) == 1
    assert ranged[0].callsign == "P3"

    sorted_planes = sort_aeroplanes(planes)
    assert [p.callsign for p in sorted_planes] == ["P2", "P3", "P1"]
    assert len(get_top_aeroplanes(sorted_planes, 2)) == 2


def test_json_saver(tmp_path) -> None:
    file_path = tmp_path / "test_planes.json"
    saver = JSONSaver(str(file_path))
    p1 = Aeroplane("SU100", "Russia", 240.0, 10500.0, "111222")

    saver.add_aeroplane(p1)
    saver.add_aeroplane(p1)
    loaded = saver.get_aeroplanes({"origin_country": "Russia"})
    assert len(loaded) == 1
    assert loaded[0].callsign == "SU100"

    saver.delete_aeroplane(p1)
    assert saver.get_aeroplanes() == []


@patch("src.api.requests.get")
def test_api_get_aeroplanes(mock_get) -> None:
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.side_effect = [
        [{"boundingbox": ["36.0", "43.8", "-9.3", "3.3"]}],
        {"states": [["345123", "IBE321", "Spain", 0, 0, -3.7, 40.4, 10000.0, False, 240.0]]},
    ]
    api = AeroplanesAPI()
    result = api.get_aeroplanes("Spain")
    assert len(result) == 1
    assert result[0][1] == "IBE321"
