from typing import Any, Dict

from fastapi import FastAPI, HTTPException

from .geometry import extract_polygons, metrics_from_polygons

app = FastAPI(title="Site Analyzer API")


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/geojson/echo")
def echo_geojson(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload


@app.post("/geojson/analyze")
def analyze_geojson(payload: Dict[str, Any]) -> Dict[str, Any]:
    polygons = extract_polygons(payload)
    if not polygons:
        raise HTTPException(status_code=400, detail="Only Polygon/MultiPolygon GeoJSON is supported.")

    try:
        metrics = metrics_from_polygons(polygons)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "area_m2": metrics.area_m2,
        "area_ping": metrics.area_m2 / 3.305785,
        "perimeter_m": metrics.perimeter_m,
        "bbox": metrics.bbox,
        "ratio": metrics.ratio,
        "compactness": metrics.compactness,
    }
