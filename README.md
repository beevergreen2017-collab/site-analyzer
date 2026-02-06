# Site Analyzer (Gate A)

獨立架構的 GIS 基地分析工具，專注 GeoJSON 幾何與分析。

## Backend (FastAPI)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Endpoints

- `GET /health` → `{ "status": "ok" }`
- `POST /geojson/echo` → 回傳原始 GeoJSON

範例:

```bash
curl -X POST http://localhost:8000/geojson/echo \
  -H "Content-Type: application/json" \
  -d '{"type":"FeatureCollection","features":[]}'
```

## Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

預設連接 `http://localhost:5173`。
