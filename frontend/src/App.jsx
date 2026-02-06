import { useMemo, useState } from "react";

const sampleGeoJSON = {
  type: "Polygon",
  coordinates: [
    [
      [0, 0],
      [30, 0],
      [30, 30],
      [0, 30],
      [0, 0]
    ]
  ]
};

const presets = {
  square: sampleGeoJSON,
  rectangle: {
    type: "Polygon",
    coordinates: [
      [
        [0, 0],
        [50, 0],
        [50, 20],
        [0, 20],
        [0, 0]
      ]
    ]
  },
  concave: {
    type: "Polygon",
    coordinates: [
      [
        [0, 0],
        [40, 0],
        [40, 10],
        [10, 10],
        [10, 30],
        [0, 30],
        [0, 0]
      ]
    ]
  }
};

function App() {
  const [geojsonText, setGeojsonText] = useState(
    JSON.stringify(sampleGeoJSON, null, 2)
  );
  const [echoResult, setEchoResult] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const parsedGeojson = useMemo(() => {
    try {
      return JSON.parse(geojsonText);
    } catch (err) {
      return null;
    }
  }, [geojsonText]);

  const handlePresetChange = (event) => {
    const preset = presets[event.target.value];
    setGeojsonText(JSON.stringify(preset, null, 2));
  };

  const callApi = async (endpoint) => {
    setError("");
    setIsLoading(true);
    try {
      const parsed = JSON.parse(geojsonText);
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(parsed)
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "API request failed.");
      }
      return data;
    } catch (err) {
      setError(err.message || "Invalid GeoJSON payload.");
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  const handleEcho = async () => {
    const data = await callApi("/geojson/echo");
    if (data) {
      setEchoResult(data);
    }
  };

  const handleAnalyze = async () => {
    const data = await callApi("/geojson/analyze");
    if (data) {
      setAnalysisResult(data);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>Site Analyzer</h1>
        <p>GIS 基地分析工具 (Gate B)</p>
      </header>
      <section>
        <h2>API Targets</h2>
        <ul>
          <li><code>GET /health</code></li>
          <li><code>POST /geojson/echo</code></li>
          <li><code>POST /geojson/analyze</code></li>
        </ul>
      </section>
      <section className="panel">
        <div>
          <h2>GeoJSON Input</h2>
          <label>
            範例
            <select onChange={handlePresetChange} defaultValue="square">
              <option value="square">Square 30x30</option>
              <option value="rectangle">Rectangle 20x50</option>
              <option value="concave">Concave Polygon</option>
            </select>
          </label>
          <textarea
            value={geojsonText}
            onChange={(event) => setGeojsonText(event.target.value)}
            rows={16}
          />
          <div className="actions">
            <button type="button" onClick={handleEcho} disabled={isLoading}>
              Echo
            </button>
            <button type="button" onClick={handleAnalyze} disabled={isLoading}>
              Analyze
            </button>
          </div>
          {error && <p className="error">{error}</p>}
        </div>
        <div className="results">
          <h2>Analysis</h2>
          {analysisResult ? (
            <div className="metrics">
              <div>
                <span>Area (m²)</span>
                <strong>{analysisResult.area_m2.toFixed(2)}</strong>
              </div>
              <div>
                <span>Area (坪)</span>
                <strong>{analysisResult.area_ping.toFixed(2)}</strong>
              </div>
              <div>
                <span>Perimeter (m)</span>
                <strong>{analysisResult.perimeter_m.toFixed(2)}</strong>
              </div>
              <div>
                <span>Ratio</span>
                <strong>{analysisResult.ratio.toFixed(2)}</strong>
              </div>
              <div>
                <span>Compactness</span>
                <strong>
                  {analysisResult.compactness === null
                    ? "N/A"
                    : analysisResult.compactness.toFixed(2)}
                </strong>
              </div>
              <div className="metric-wide">
                <span>BBox</span>
                <strong>{JSON.stringify(analysisResult.bbox)}</strong>
              </div>
            </div>
          ) : (
            <p className="muted">尚未分析，請點擊 Analyze。</p>
          )}
          <h2>Echo Result</h2>
          <pre>{JSON.stringify(echoResult ?? parsedGeojson, null, 2)}</pre>
        </div>
      </section>
    </div>
  );
}

export default App;
