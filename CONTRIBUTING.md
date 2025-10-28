## Contributing to AI Agents for Google Earth Engine

Thank you for helping build open-source GeoAI. This guide explains how to add a new agent and improve the project.

### Workflow

- Fork the repo
- Create a branch: `git checkout -b feat/<agent-name>`
- Add your agent under `agents/<agent-name>` (structure below)
- Run and validate your example notebook
- Open a PR with a clear description

### Required agent structure

```
agents/
  <agent-name>/
    tools/
      <your_tools>.py
    agent.yaml
    main.py
    requirements.txt
    example.ipynb
    README.md
```

### Agent metadata (minimum)

```yaml
name: <string>
version: <semver>
description: <what the agent does>
authors:
  - name: <string>
    email: <string>
license: MIT
framework: strands
entrypoint: main.py:<AgentClass>
tags: [gee, your, tags]
dependencies: [strands, geemap, earthengine-api, leafmap]
runtime:
  python: ">=3.10"
parameters:
  # optional: declare your expected inputs
```

### Coding standards

- Python >= 3.10
- PEP 8 + type hints + docstrings
- Each tool is a pure function decorated with `@tool`
- Agents subclass `strands.Agent` and expose a discoverable entrypoint

### Earth Engine usage

- Prefer public datasets and open assets
- Do not commit private asset IDs or tokens
- Document data sources in the agent `README.md`

### PR checklist

- [ ] `agent.yaml` present and valid
- [ ] `main.py` subclasses `strands.Agent`
- [ ] `tools/` contains at least one `@tool`
- [ ] `requirements.txt` lists exact runtime deps
- [ ] `example.ipynb` runs end-to-end (Colab-friendly)
- [ ] Agent `README.md` explains usage and parameters
- [ ] No secrets; follows Code of Conduct

### Communication

Use the repository Discussions tab for questions and ideas. Please be respectful and collaborative.
