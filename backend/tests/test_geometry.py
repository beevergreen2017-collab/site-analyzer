from backend.geometry import extract_polygons, metrics_from_polygons


def test_square_30x30() -> None:
    geojson = {
        "type": "Polygon",
        "coordinates": [[[0, 0], [30, 0], [30, 30], [0, 30], [0, 0]]],
    }
    polygons = extract_polygons(geojson)
    metrics = metrics_from_polygons(polygons)
    assert metrics.area_m2 == 900
    assert metrics.perimeter_m == 120
    assert metrics.bbox == [0, 0, 30, 30]
    assert metrics.ratio == 1


def test_rectangle_20x50() -> None:
    geojson = {
        "type": "Polygon",
        "coordinates": [[[0, 0], [50, 0], [50, 20], [0, 20], [0, 0]]],
    }
    polygons = extract_polygons(geojson)
    metrics = metrics_from_polygons(polygons)
    assert metrics.area_m2 == 1000
    assert metrics.perimeter_m == 140
    assert metrics.bbox == [0, 0, 50, 20]
    assert metrics.ratio == 2.5


def test_concave_polygon() -> None:
    geojson = {
        "type": "Polygon",
        "coordinates": [[[0, 0], [40, 0], [40, 10], [10, 10], [10, 30], [0, 30], [0, 0]]],
    }
    polygons = extract_polygons(geojson)
    metrics = metrics_from_polygons(polygons)
    assert metrics.area_m2 == 600
    assert metrics.perimeter_m == 140
    assert metrics.bbox == [0, 0, 40, 30]
    assert metrics.ratio == max(40 / 30, 30 / 40)
