## flood_mapper

Compute NDWI over a user-provided AOI and date range using the Google Earth Engine Sentinel-2 collection. Ships as a Strands agent with reusable tools.

### Features

- Loads Sentinel‑2 imagery from GEE with cloud filtering
- Computes NDWI = (Green − NIR) / (Green + NIR)
- Returns a preview URL and stats; interactive map in the notebook

### Install

```
pip install -r requirements.txt
```

### Usage

```python
from main import FloodMapperAgent

agent = FloodMapperAgent()
result = agent.run(
    aoi=[-122.6, 37.6, -122.2, 37.9],  # minx, miny, maxx, maxy (San Francisco Bay)
    start_date="2023-01-01",
    end_date="2023-02-01",
    cloud_pct=20,
)
print(result)
```

Run a script and generate an HTML map:

```
python example.py
```

`ndwi_map.html` will be created in the current folder.

Or open `example.ipynb` for an interactive walk-through.

### Parameters

- `aoi`: GeoJSON Polygon or `[minx, miny, maxx, maxy]` list
- `start_date`, `end_date`: ISO date strings
- `cloud_pct`: maximum cloud percentage (default 20)

### Data sources

- Sentinel‑2 Level‑2A (`COPERNICUS/S2_SR`)

### License

MIT
