from __future__ import annotations

from dataclasses import dataclass
from math import dist
from typing import Iterable, List, Sequence


Coordinate = Sequence[float]
Ring = List[Coordinate]
Polygon = List[Ring]


@dataclass(frozen=True)
class GeometryMetrics:
    area_m2: float
    perimeter_m: float
    bbox: List[float]
    ratio: float
    compactness: float | None


def _ring_area(ring: Ring) -> float:
    if len(ring) < 3:
        return 0.0
    total = 0.0
    for idx, point in enumerate(ring):
        next_point = ring[(idx + 1) % len(ring)]
        total += point[0] * next_point[1] - next_point[0] * point[1]
    return total / 2.0


def _ring_perimeter(ring: Ring) -> float:
    if len(ring) < 2:
        return 0.0
    total = 0.0
    for idx, point in enumerate(ring):
        next_point = ring[(idx + 1) % len(ring)]
        total += dist(point, next_point)
    return total


def _iter_coords(polygons: Iterable[Polygon]) -> Iterable[Coordinate]:
    for polygon in polygons:
        for ring in polygon:
            for coord in ring:
                yield coord


def _bbox_from_coords(coords: Iterable[Coordinate]) -> List[float]:
    iterator = iter(coords)
    first = next(iterator)
    min_x = max_x = first[0]
    min_y = max_y = first[1]
    for coord in iterator:
        min_x = min(min_x, coord[0])
        max_x = max(max_x, coord[0])
        min_y = min(min_y, coord[1])
        max_y = max(max_y, coord[1])
    return [min_x, min_y, max_x, max_y]


def metrics_from_polygons(polygons: Iterable[Polygon]) -> GeometryMetrics:
    polygons_list = list(polygons)
    if not polygons_list:
        raise ValueError("No polygon coordinates provided.")

    area_m2 = 0.0
    perimeter_m = 0.0
    for polygon in polygons_list:
        if not polygon:
            continue
        outer = polygon[0]
        area_m2 += abs(_ring_area(outer))
        perimeter_m += _ring_perimeter(outer)
        for hole in polygon[1:]:
            area_m2 -= abs(_ring_area(hole))
            perimeter_m += _ring_perimeter(hole)

    if area_m2 < 0:
        area_m2 = 0.0

    bbox = _bbox_from_coords(_iter_coords(polygons_list))
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    if width == 0 or height == 0:
        ratio = float("inf")
    else:
        ratio = max(width / height, height / width)

    compactness = None if area_m2 == 0 else (perimeter_m**2) / area_m2

    return GeometryMetrics(
        area_m2=area_m2,
        perimeter_m=perimeter_m,
        bbox=bbox,
        ratio=ratio,
        compactness=compactness,
    )


def extract_polygons(geojson: dict) -> List[Polygon]:
    geo_type = geojson.get("type")
    if geo_type == "FeatureCollection":
        polygons: List[Polygon] = []
        for feature in geojson.get("features", []):
            polygons.extend(extract_polygons(feature))
        return polygons
    if geo_type == "Feature":
        geometry = geojson.get("geometry") or {}
        return extract_polygons(geometry)
    if geo_type == "Polygon":
        return [geojson.get("coordinates", [])]
    if geo_type == "MultiPolygon":
        return geojson.get("coordinates", [])
    return []
