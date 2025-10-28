## AI Agents for Google Earth Engine (GEE)

Community-driven Strands agents for geospatial analysis and visualization with Google Earth Engine. This repository provides a clear framework for discovering, developing, and sharing AI agents that use GEE following Strands conventions.

### Why this project?

- **Open GeoAI**: Accelerate reproducible geospatial analytics by packaging workflows as portable agents.
- **Strands-native**: Each agent ships with `agent.yaml` metadata, `@tool`-decorated tools, and a subclass of `strands.Agent`.
- **GEE-first**: Examples use the Earth Engine Python API with friendly visualization via `geemap`/`leafmap`.

### Repository layout

```
agents/
  flood_mapper/
    tools/
    agent.yaml
    main.py
    requirements.txt
    example.ipynb
    README.md
.gitignore
CODE_OF_CONDUCT.md
CONTRIBUTING.md
LICENSE
pyproject.toml
README.md
```

### Quick start

1. Python >= 3.10 recommended. Create a virtual environment.
2. Try the sample agent:

```
cd agents/flood_mapper
pip install -r requirements.txt
python -c "from main import FloodMapperAgent; agent=FloodMapperAgent(); print(agent.run_demo())"
```

3. Open `example.ipynb` to run an interactive map. For first-time Earth Engine users, authenticate when prompted.

### Agent metadata schema (example)

```yaml
name: flood_mapper
version: 0.1.0
description: Compute NDWI over an AOI/date range using GEE and visualize results.
authors:
  - name: Your Name
    email: you@example.com
license: MIT
framework: strands
entrypoint: main.py:FloodMapperAgent
tags: [gee, ndwi, sentinel-2, water]
dependencies:
  - strands
  - geemap
  - earthengine-api
  - leafmap
runtime:
  python: ">=3.10"
parameters:
  aoi: { type: Polygon, description: GeoJSON polygon or bbox list }
  start_date: { type: string, description: ISO date }
  end_date: { type: string, description: ISO date }
  cloud_pct: { type: number, default: 20 }
```

### Contribution workflow

1. Fork → 2) create feature branch → 3) add your agent under `agents/<your_agent>` → 4) include `agent.yaml`, `main.py`, `tools/`, `requirements.txt`, `README.md`, and an `example.ipynb` → 5) open a Pull Request → 6) review.

See `CONTRIBUTING.md` for details (validation checklist, testing, and review standards).

### Coding standards

- PEP 8, type hints, and concise docstrings.
- Tools must be declared with `@tool` and be importable.
- Agents must subclass `strands.Agent` and expose a clear entrypoint.

### Ethical rules

- Use only open/public datasets and assets.
- Exclude secrets and private Earth Engine assets from commits.

### Community

- Start or join discussions in the repository’s Discussions tab.
- Cite and recognize contributors in agent `README.md` files.

### License

MIT. See `LICENSE`.
