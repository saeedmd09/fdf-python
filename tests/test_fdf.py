import pytest

from fdf.model import Map, Point
from fdf.parser import MapFormatError, parse_map
from fdf.projection import Camera


def test_parse_elem():
    map_data = parse_map("maps/elem.fdf")
    assert map_data.width == 5
    assert map_data.height == 5
    assert map_data.points[2][2].z == 5


@pytest.mark.parametrize(
    "value, expected_z, expected_color",
    [
        ("7", 7, None),
        ("-3", -3, None),
        ("2,0xFF8800", 2, "#FF8800"),
        ("1,0xff", 1, "#0000FF"),
    ],
)
def test_parse_values(value, expected_z, expected_color, tmp_path):
    file_path = tmp_path / "test.fdf"
    file_path.write_text(value, encoding="utf-8")

    map_data = parse_map(file_path)
    point = map_data.points[0][0]

    assert point.z == expected_z
    assert point.color == expected_color


@pytest.mark.parametrize(
    "content",
    [
        "",
        "1 2\n3",
        "1 x",
        "1,invalid",
        "1,0x1234567",
    ],
)
def test_invalid_maps(content, tmp_path):
    file_path = tmp_path / "bad.fdf"
    file_path.write_text(content, encoding="utf-8")

    with pytest.raises(MapFormatError):
        parse_map(file_path)


def test_map_length_and_iteration():
    points = [
        [Point(0, 0, 0), Point(1, 0, 0)],
        [Point(0, 1, 0), Point(1, 1, 0)],
    ]

    map_data = Map(points)

    assert len(map_data) == 4
    assert len(list(map_data)) == 4


def test_neighbors():
    points = [
        [Point(0, 0, 0), Point(1, 0, 0)],
        [Point(0, 1, 0), Point(1, 1, 0)],
    ]

    map_data = Map(points)

    assert len(map_data.neighbors(points[0][0])) == 2


def test_projection_origin():
    camera = Camera()
    point = Point(0, 0, 0)

    assert camera.project(point) == (0.0, 0.0)


def test_projection_height():
    camera = Camera()
    point = Point(0, 0, 1)

    assert camera.project(point)[1] < 0


def test_camera_fit():
    map_data = parse_map("maps/elem.fdf")
    camera = Camera()
    camera.fit(map_data, 800, 600)

    for point in map_data:
        x, y = camera.project(point)
        assert 0 <= x <= 800
        assert 0 <= y <= 600