# CityLab AI — Autonomous Urban Policy Sandbox

A multi-agent urban simulator where LLM-driven stakeholder agents (residents, transit operators, planners, businesses, emergency services) test policies, infrastructure changes, and events in a sandboxed digital twin of a city — producing explainable outcomes, tradeoffs, and actionable recommendations.

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Running Locally](#running-locally)
- [Quickstart (Docker)](#quickstart-docker)
- [Docker Deployment](#docker-deployment)
- [API](#api)
- [MVP Features](#mvp-features)
- [Evaluation Metrics](#evaluation-metrics)
- [Safety and Ethics](#safety-and-ethics)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

## Project Overview

This system combines real-world urban data with multi-agent simulation to enable policy makers, urban planners, and researchers to test the potential impacts of urban policies before implementation. The platform uses large language models (LLMs) to drive intelligent agent behaviors, allowing for realistic simulations of how different stakeholders might respond to policy changes.

### Key Features

- **Real-world data integration**: Combines GIS maps, transit networks, population data, and historical events
- **Multi-agent reasoning**: LLMs act as cognitive controllers for heterogeneous agents that interpret goals, read policy docs, negotiate, and generate structured actions
- **Scenario experimentation**: "What if?" experiments at city scale with human-in-the-loop validation
- **Explainable AI**: Every agent decision links back to evidence (policy docs, simulation traces, retrieved sources)

## System Architecture

### Frontend
- **Next.js** + **Mapbox/Deck.gl** for interactive geospatial visualization
- Real-time dashboards and scenario editors
- Time slider for simulation playback

### Backend
- **FastAPI** (Python) for simulation control and API endpoints
- **LangChain/LlamaIndex** for agent orchestration and RAG
- **Mesa** for agent-based modeling
- **Celery + Redis** for background jobs
- **PostgreSQL** for scenario metadata and time series
- **Pinecone/Chroma** for vector storage (policy/document embeddings)

### Agent Ecosystem
- **Resident Agents**: Household schedules, mode choice, respond to changes
- **Transit Operator**: Adjusts routes/frequencies, budget management
- **Planner/Policy Agent**: Proposes rules, reads legislation via RAG
- **Developer/Business Agent**: Location decisions, pricing, zoning reactions
- **Emergency Services**: Incident response, resource allocation
- **Orchestrator**: Coordinates simulation, manages scenarios, aggregates KPIs

## Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL
- Redis
- Docker (optional)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

### Environment Variables
Create `.env` files in both `backend/` and `frontend/` directories. See `.env.example` files for required variables.

## Running Locally

### Backend
```bash
cd backend
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm run dev
```

### Celery Worker (for background jobs)
```bash
cd backend
celery -A app.celery_app worker --loglevel=info
```

## Quickstart (Docker)

If you want to run everything locally with the fewest steps, use Docker Compose.

1. Create a root `.env` file (optional but recommended):

```bash
export OPENAI_API_KEY=your_key_here
export ANTHROPIC_API_KEY=your_key_here
export NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token_here
```

2. Start services:

```bash
docker-compose up -d
```

3. Run database migrations:

```bash
docker-compose exec backend alembic upgrade head
```

4. Open:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API docs: `http://localhost:8000/api/docs`

## Docker Deployment

```bash
docker-compose up -d
```

## API

The backend serves OpenAPI docs at:
- `http://localhost:8000/api/docs`

Common endpoints:
- `GET /api/v1/scenarios/`: list scenarios
- `POST /api/v1/scenarios/`: create a scenario
- `POST /api/v1/scenarios/{scenario_id}/runs`: start a simulation run (triggers Celery task)

Example: create a scenario

```bash
curl -X POST "http://localhost:8000/api/v1/scenarios/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bus priority lane (demo)",
    "description": "Basic demo scenario for a bus-priority policy",
    "policy_type": "bus_priority",
    "policy_config": {"corridor_id": "demo", "lane_hours": "07:00-19:00"}
  }'
```

## MVP Features

- Import street graphs and POIs from OpenStreetMap
- Resident agents with commuter schedules and route choice
- Transit operator agent with route/frequency adjustments
- Scenario runner: simulate N days, collect KPIs
- Interactive map visualization with time slider
- Explainability: agent actions annotated with prompts/retrieved docs

## Evaluation Metrics

- Policy impact: % change in commute time, transit modal share, emissions
- Equity indices: access to jobs within 30 min
- Simulation realism: validation vs historical baseline
- Explainability score: quality of LLM rationales

## Safety & Ethics

- All outputs labeled as simulated projections (not predictions)
- Confidence ranges and provenance provided
- Human review required for real policy decisions
- Privacy protection for sensitive municipal data

## License

MIT License

## Contributing

Contributions welcome! Please read our contributing guidelines first.

## Contact

For questions or partnerships, please open an issue or contact the maintainers.
