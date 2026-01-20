# CityLab AI — Autonomous Urban Policy Sandbox

A multi-agent urban simulator where LLM-driven stakeholder agents (residents, transit operators, planners, businesses, emergency services) test policies, infrastructure changes, and events in a sandboxed digital twin of a city — producing explainable outcomes, tradeoffs, and actionable recommendations.

## 🚀 Why This is Mind-Blowing

- **Real-world data integration**: Combines GIS maps, transit networks, population data, and historical events
- **Multi-agent reasoning**: LLMs act as cognitive controllers for heterogeneous agents that interpret goals, read policy docs, negotiate, and generate structured actions
- **Scenario experimentation**: "What if?" experiments at city scale with human-in-the-loop validation
- **Explainable AI**: Every agent decision links back to evidence (policy docs, simulation traces, retrieved sources)

## 🏗️ Architecture

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

## 📦 Installation

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

## 🚀 Running Locally

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

## 🐳 Docker Deployment

```bash
docker-compose up -d
```

## 📊 MVP Features

- Import street graphs and POIs from OpenStreetMap
- Resident agents with commuter schedules and route choice
- Transit operator agent with route/frequency adjustments
- Scenario runner: simulate N days, collect KPIs
- Interactive map visualization with time slider
- Explainability: agent actions annotated with prompts/retrieved docs

## 🔬 Evaluation Metrics

- Policy impact: % change in commute time, transit modal share, emissions
- Equity indices: access to jobs within 30 min
- Simulation realism: validation vs historical baseline
- Explainability score: quality of LLM rationales

## 🛡️ Safety & Ethics

- All outputs labeled as simulated projections (not predictions)
- Confidence ranges and provenance provided
- Human review required for real policy decisions
- Privacy protection for sensitive municipal data

## 📝 License

MIT License

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines first.

## 📧 Contact

For questions or partnerships, please open an issue or contact the maintainers.
