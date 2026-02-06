from typing import Any, Dict

from fastapi import FastAPI

app = FastAPI(title="Site Analyzer API")


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/geojson/echo")
def echo_geojson(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload
