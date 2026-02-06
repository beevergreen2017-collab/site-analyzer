const sampleGeoJSON = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [121.5654, 25.033]
      },
      properties: {
        name: "Sample Site"
      }
    }
  ]
};

function App() {
  return (
    <div className="app">
      <header>
        <h1>Site Analyzer</h1>
        <p>GIS 基地分析工具 (Gate A)</p>
      </header>
      <section>
        <h2>API Targets</h2>
        <ul>
          <li><code>GET /health</code></li>
          <li><code>POST /geojson/echo</code></li>
        </ul>
      </section>
      <section>
        <h2>GeoJSON Preview</h2>
        <pre>{JSON.stringify(sampleGeoJSON, null, 2)}</pre>
      </section>
    </div>
  );
}

export default App;
