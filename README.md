# 🏙️ CityLab AI — Autonomous Urban Policy Sandbox

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

> **A multi-agent urban simulator where LLM-driven stakeholder agents test policies, infrastructure changes, and events in a sandboxed digital twin of a city — producing explainable outcomes, tradeoffs, and actionable recommendations.**

Think of it as **SimCity meets ChatGPT** — but for real urban planning decisions.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Quick Start (Docker)](#quick-start-docker)
  - [Manual Installation](#manual-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Agent Ecosystem](#-agent-ecosystem)
- [Evaluation Metrics](#-evaluation-metrics)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Safety & Ethics](#-safety--ethics)
- [License](#-license)
- [Support](#-support)

---

## 🎯 Overview

**CityLab AI** is an open-source platform that combines real-world urban data with multi-agent simulation to enable policy makers, urban planners, and researchers to test the potential impacts of urban policies before implementation. 

The platform uses **Large Language Models (LLMs)** as cognitive controllers for intelligent agents, allowing for realistic simulations of how different stakeholders might respond to policy changes.

### Why This Matters

- **Evidence-Based Planning**: Test policies before implementation
- **Stakeholder Simulation**: Understand how different groups react to changes
- **Explainable AI**: Every decision is traceable and justified
- **Real-World Data**: Built on actual city infrastructure and demographics
- **Cost-Effective**: Identify issues in simulation rather than production

---

## ✨ Key Features

### 🗺️ Real-World Data Integration
- Import GIS maps, transit networks, and population data
- OpenStreetMap integration out of the box
- Support for custom city datasets
- Historical event analysis

### 🤖 Multi-Agent Reasoning with LLMs
- LLMs act as **cognitive controllers** for heterogeneous agents
- Agents interpret goals, read policy documents, and negotiate
- Each agent has unique persona, memory, and decision-making
- Powered by GPT-4, Claude, and other state-of-the-art models

### 🧪 Scenario Experimentation
- Run "what if?" experiments at city scale
- Test policies like:
  - Congestion pricing
  - Bus-priority lanes
  - Zoning changes
  - Transit route modifications
  - Infrastructure investments
- Human-in-the-loop validation

### 📊 Explainable AI
- Every agent decision links to evidence
- Policy documents and simulation traces
- LLM-generated rationales for actions
- Full provenance tracking
- Confidence intervals on predictions

### 📈 Interactive Visualization
- Real-time geospatial dashboards
- Time-slider for simulation playback
- Metrics tracking and comparison
- Export reports with citations

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│  Next.js 14 + TypeScript + Mapbox/Deck.gl + Tailwind CSS   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                       │
│              FastAPI + OpenAPI Documentation                 │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
┌───────────────────────────┐   ┌──────────────────────────┐
│   Agent Orchestration     │   │   Background Jobs        │
│  LangChain + LlamaIndex   │   │  Celery + Redis Queue    │
│  Multi-Agent Coordination │   │  Async Task Processing   │
└───────────────────────────┘   └──────────────────────────┘
                │                           │
                ▼                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Simulation Engine                         │
│        Mesa Agent-Based Modeling + NetworkX Graphs          │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐   ┌──────────────────┐   ┌────────────────┐
│  PostgreSQL  │   │  Vector Store    │   │  Redis Cache   │
│  Time Series │   │  Chroma/Pinecone │   │  Session Data  │
│  Scenarios   │   │  Policy Docs     │   │  Real-time     │
└──────────────┘   └──────────────────┘   └────────────────┘
```

### Component Breakdown

**Frontend**
- **Next.js 14** with App Router for modern React development
- **Mapbox GL JS** + **Deck.gl** for interactive 3D geospatial visualization
- **Recharts** for metrics dashboards and time-series plots
- **Zustand** for state management
- **React Query** for data fetching and caching

**Backend**
- **FastAPI** for high-performance async API endpoints
- **LangChain/LlamaIndex** for LLM orchestration and RAG pipelines
- **Mesa** for agent-based modeling framework
- **Celery** for distributed task queue
- **SQLAlchemy** for ORM and database management
- **Alembic** for database migrations

**Data Layer**
- **PostgreSQL 15+** for relational data and time series
- **Redis 7+** for caching and message broker
- **Chroma/Pinecone** for vector embeddings and semantic search
- **NetworkX** for graph-based city network modeling

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose | Version |
|------------|---------|---------|
| Python | Core language | 3.10+ |
| FastAPI | Web framework | 0.104+ |
| LangChain | LLM orchestration | 0.1.0+ |
| LlamaIndex | RAG framework | 0.9.30+ |
| Mesa | Agent-based modeling | 2.1.1+ |
| Celery | Task queue | 5.3.4+ |
| SQLAlchemy | ORM | 2.0.23+ |
| PostgreSQL | Database | 15+ |
| Redis | Cache & broker | 7+ |

### Frontend
| Technology | Purpose | Version |
|------------|---------|---------|
| Next.js | React framework | 14.0.4 |
| TypeScript | Type safety | 5.3+ |
| Mapbox GL | Map rendering | 3.0+ |
| Deck.gl | 3D visualization | 9.0+ |
| Recharts | Charts | 2.10+ |
| Tailwind CSS | Styling | 3.4+ |

### AI/ML
| Technology | Purpose |
|------------|---------|
| OpenAI GPT-4 | Primary LLM |
| Anthropic Claude | Alternative LLM |
| Chroma | Vector database |
| Pinecone | Cloud vector DB (optional) |

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **PostgreSQL 15+** ([Download](https://www.postgresql.org/download/))
- **Redis 7+** ([Download](https://redis.io/download))
- **Docker & Docker Compose** (optional, recommended) ([Download](https://www.docker.com/))

You'll also need API keys for:
- **OpenAI API** ([Get key](https://platform.openai.com/api-keys))
- **Anthropic API** (optional) ([Get key](https://console.anthropic.com/))
- **Mapbox** ([Get token](https://account.mapbox.com/access-tokens/))

### Quick Start (Docker)

The fastest way to get CityLab AI running locally:

1. **Clone the repository:**
```bash
git clone https://github.com/fanisridhar/CityLab-AI---Autonomous-Urban-Policy-Sandbox.git
cd CityLab-AI---Autonomous-Urban-Policy-Sandbox
```

2. **Set up environment variables:**
```bash
# Create .env file in project root
cat > .env << EOF
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token_here
EOF
```

3. **Start all services:**
```bash
docker-compose up -d
```

4. **Run database migrations:**
```bash
docker-compose exec backend alembic upgrade head
```

5. **Access the application:**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Celery Flower** (task monitoring): http://localhost:5555

6. **Stop services:**
```bash
docker-compose down
```

### Manual Installation

For development or custom setups:

#### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create and activate virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Set up PostgreSQL database:**
```bash
# Create database
createdb citylab_db

# Run migrations
alembic upgrade head
```

6. **Start Redis:**
```bash
redis-server
```

7. **Start backend server:**
```bash
uvicorn app.main:app --reload
```

8. **Start Celery worker (in a new terminal):**
```bash
cd backend
source venv/bin/activate
celery -A app.celery_app worker --loglevel=info
```

#### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Set up environment variables:**
```bash
cp .env.example .env.local
# Edit .env.local with your configuration
```

4. **Start development server:**
```bash
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

---

## 📖 Usage

### Creating Your First Scenario

1. **Access the web interface** at http://localhost:3000

2. **Create a new scenario:**
   - Click "New Scenario"
   - Enter scenario name and description
   - Select policy type (e.g., "Bus Priority Lane")
   - Configure policy parameters

3. **Run the simulation:**
   - Click "Run Simulation"
   - Set simulation duration (e.g., 30 days)
   - Monitor progress in real-time

4. **Analyze results:**
   - View metrics dashboard
   - Explore map visualization
   - Review agent decisions and rationales
   - Export report with findings

### Using the API

Create a scenario via API:

```bash
curl -X POST "http://localhost:8000/api/v1/scenarios/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bus Priority Lane Demo",
    "description": "Test impact of dedicated bus lanes on Main Street",
    "policy_type": "bus_priority",
    "policy_config": {
      "corridor_id": "main_street",
      "lane_hours": "07:00-19:00",
      "enforcement": true
    }
  }'
```

Start a simulation run:

```bash
curl -X POST "http://localhost:8000/api/v1/scenarios/{scenario_id}/runs" \
  -H "Content-Type: application/json" \
  -d '{
    "duration_days": 30,
    "time_step_minutes": 15
  }'
```

---

## 📚 API Documentation

### Interactive API Docs

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Key Endpoints

#### Scenarios
- `GET /api/v1/scenarios/` - List all scenarios
- `POST /api/v1/scenarios/` - Create new scenario
- `GET /api/v1/scenarios/{id}` - Get scenario details
- `PUT /api/v1/scenarios/{id}` - Update scenario
- `DELETE /api/v1/scenarios/{id}` - Delete scenario

#### Simulations
- `POST /api/v1/scenarios/{id}/runs` - Start simulation
- `GET /api/v1/simulations/{id}` - Get simulation status
- `GET /api/v1/simulations/{id}/results` - Get results
- `POST /api/v1/simulations/{id}/stop` - Stop simulation

#### Agents
- `GET /api/v1/agents/` - List agent types
- `GET /api/v1/agents/{id}/decisions` - Get agent decision history
- `GET /api/v1/agents/{id}/rationale` - Get decision explanations

#### Data
- `POST /api/v1/data/import/osm` - Import OpenStreetMap data
- `GET /api/v1/data/city/{city_id}` - Get city data
- `POST /api/v1/data/upload` - Upload custom datasets

---

## 🤖 Agent Ecosystem

### Agent Types

#### 1. **Resident Agents**
- **Role**: Represent individual households and commuters
- **Behaviors**:
  - Daily activity scheduling (work, shopping, leisure)
  - Transportation mode choice (car, transit, bike, walk)
  - Route selection based on time, cost, comfort
  - Response to policy changes (pricing, infrastructure)
- **Decision Factors**: Travel time, cost, convenience, safety

#### 2. **Transit Operator Agent**
- **Role**: Manages public transportation system
- **Behaviors**:
  - Route planning and frequency adjustments
  - Budget allocation across routes
  - Response to ridership changes
  - Service quality optimization
- **Decision Factors**: Ridership, revenue, coverage, equity

#### 3. **Planner/Policy Agent**
- **Role**: Proposes and evaluates urban policies
- **Behaviors**:
  - Reads legislation and policy documents via RAG
  - Proposes new regulations
  - Evaluates policy impacts
  - Budget constraint management
- **Decision Factors**: Public benefit, cost, feasibility, equity

#### 4. **Developer/Business Agent**
- **Role**: Represents private sector interests
- **Behaviors**:
  - Location decisions for new developments
  - Pricing strategies
  - Response to zoning changes
  - Investment decisions
- **Decision Factors**: Profitability, market demand, regulations

#### 5. **Emergency Services Agent**
- **Role**: Manages emergency response
- **Behaviors**:
  - Incident response coordination
  - Resource allocation
  - Route optimization for emergency vehicles
  - Response time evaluation
- **Decision Factors**: Response time, coverage, resource availability

#### 6. **Orchestrator Agent**
- **Role**: Coordinates the entire simulation
- **Behaviors**:
  - Manages simulation clock and time steps
  - Coordinates agent interactions
  - Aggregates metrics and KPIs
  - Handles scenario rollout
- **Decision Factors**: Simulation stability, data consistency

### Agent Communication

Agents communicate through:
- **Direct messaging**: Agent-to-agent negotiations
- **Broadcast events**: System-wide announcements
- **Shared state**: Access to city model and metrics
- **RAG queries**: Retrieve relevant policy documents

---

## 📊 Evaluation Metrics

### Transportation Metrics
- **Average Commute Time**: Mean travel time for all trips
- **Transit Modal Share**: % of trips using public transit
- **Transit Ridership**: Daily passenger counts
- **Vehicle Miles Traveled (VMT)**: Total distance driven
- **Congestion Index**: Traffic delay metrics

### Equity Metrics
- **Job Accessibility**: % population with 30-min access to jobs
- **Service Coverage**: % population within 400m of transit
- **Affordability Index**: Transportation cost as % of income
- **Spatial Equity**: Distribution of benefits across neighborhoods

### Environmental Metrics
- **CO2 Emissions**: Estimated carbon footprint
- **Air Quality Index**: Pollution levels
- **Energy Consumption**: Total energy used for transportation

### Economic Metrics
- **Transit Revenue**: Fare collection
- **Operating Costs**: System maintenance and operations
- **Cost-Benefit Ratio**: Economic efficiency
- **Property Values**: Impact on real estate

### Policy Impact Metrics
- **Adoption Rate**: % of population affected by policy
- **Compliance Rate**: % following new regulations
- **Satisfaction Score**: Agent-reported satisfaction
- **Unintended Consequences**: Unexpected outcomes

---

## 📁 Project Structure

```
CityLab-AI/
├── backend/                      # FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry
│   │   ├── agents/              # LLM-driven agent controllers
│   │   │   ├── __init__.py
│   │   │   ├── base.py          # Base agent class
│   │   │   ├── orchestrator.py  # Simulation coordinator
│   │   │   ├── planner.py       # Policy agent
│   │   │   ├── resident.py      # Household agent
│   │   │   └── transit_operator.py
│   │   ├── api/                 # API routes
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── agents.py    # Agent endpoints
│   │   │       ├── data.py      # Data import/export
│   │   │       ├── explainability.py
│   │   │       ├── scenarios.py # Scenario CRUD
│   │   │       └── simulations.py
│   │   ├── core/                # Core configuration
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py   # Celery configuration
│   │   │   ├── config.py        # Settings
│   │   │   ├── database.py      # DB connection
│   │   │   └── redis_client.py  # Redis connection
│   │   ├── data_ingestion/      # Data loaders
│   │   │   ├── __init__.py
│   │   │   └── osm_loader.py    # OpenStreetMap import
│   │   ├── models/              # SQLAlchemy models
│   │   │   └── (database models)
│   │   ├── rag/                 # Retrieval-Augmented Generation
│   │   │   ├── __init__.py
│   │   │   ├── retriever.py     # Document retrieval
│   │   │   └── vector_store.py  # Vector DB interface
│   │   ├── simulation/          # Simulation engine
│   │   │   ├── __init__.py
│   │   │   ├── city_model.py    # Mesa city model
│   │   │   └── simulation_engine.py
│   │   └── tasks/               # Celery tasks
│   │       ├── __init__.py
│   │       ├── data_ingestion.py
│   │       ├── rag.py
│   │       └── simulation.py
│   ├── alembic/                 # Database migrations
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   ├── tests/                   # Backend tests
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_main.py
│   │   └── test_models.py
│   ├── .env.example
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── pytest.ini
│   └── requirements.txt
│
├── frontend/                    # Next.js frontend
│   ├── app/                     # App router
│   │   ├── globals.css
│   │   ├── layout.tsx           # Root layout
│   │   └── page.tsx             # Home page
│   ├── components/              # React components
│   │   ├── MapVisualization.tsx # Mapbox/Deck.gl map
│   │   ├── MetricsDashboard.tsx # Charts and KPIs
│   │   ├── ScenarioPanel.tsx    # Scenario editor
│   │   └── TimeSlider.tsx       # Simulation timeline
│   ├── public/                  # Static assets
│   ├── .env.example
│   ├── .eslintrc.json
│   ├── .gitignore
│   ├── Dockerfile
│   ├── next.config.js
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── .gitignore
├── docker-compose.yml           # Docker orchestration
├── DEPLOYMENT.md                # Deployment guide
├── LICENSE                      # MIT License
├── README.md                    # This file
└── REDDIT_DESCRIPTION.md        # Community description
```

---

## 🚢 Deployment

### Production Deployment

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

#### Recommended Platforms

**Backend:**
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- Railway
- Render

**Frontend:**
- Vercel (optimized for Next.js)
- Netlify
- AWS Amplify
- Cloudflare Pages

**Database:**
- AWS RDS (PostgreSQL)
- Google Cloud SQL
- Azure Database for PostgreSQL
- Supabase

**Vector Database:**
- Pinecone (managed)
- Chroma (self-hosted)
- Weaviate (cloud or self-hosted)

#### Environment Variables

**Backend (.env):**
```bash
DATABASE_URL=postgresql://user:pass@host:5432/dbname
REDIS_URL=redis://host:6379/0
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
SECRET_KEY=your-secret-key
ALLOWED_ORIGINS=https://yourdomain.com
```

**Frontend (.env.local):**
```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_MAPBOX_TOKEN=pk.eyJ1...
```

#### Docker Production Build

```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose exec backend alembic upgrade head
```

---

## 🗺️ Roadmap

### Phase 1: MVP (Current)
- [x] Basic agent framework
- [x] OpenStreetMap integration
- [x] Resident and transit operator agents
- [x] Scenario management
- [x] Interactive map visualization
- [x] Basic metrics dashboard

### Phase 2: Enhanced Agents (Q2 2024)
- [ ] Developer/business agent implementation
- [ ] Emergency services agent
- [ ] More sophisticated agent behaviors
- [ ] Agent learning and adaptation
- [ ] Multi-agent negotiation protocols

### Phase 3: Advanced Features (Q3 2024)
- [ ] Historical data validation
- [ ] Multi-city support
- [ ] Collaborative scenario editing
- [ ] Advanced policy types (zoning, parking, bike infrastructure)
- [ ] Real-time data integration
- [ ] Mobile app for field validation

### Phase 4: Enterprise Features (Q4 2024)
- [ ] White-label deployment
- [ ] Custom agent development SDK
- [ ] Advanced analytics and reporting
- [ ] Integration with GIS platforms
- [ ] API marketplace for extensions
- [ ] Enterprise support and SLAs

### Future Considerations
- Climate change scenario modeling
- Economic impact analysis
- Social equity optimization
- Integration with smart city IoT
- AR/VR visualization
- Blockchain for transparent decision tracking

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

1. **Code Contributions**
   - Bug fixes
   - New features
   - Performance improvements
   - Test coverage

2. **Documentation**
   - Improve README and guides
   - Add code comments
   - Create tutorials
   - Translate documentation

3. **Testing**
   - Report bugs
   - Test new features
   - Validate simulations
   - Performance testing

4. **Design**
   - UI/UX improvements
   - Visualization enhancements
   - Accessibility improvements

5. **Research**
   - Agent behavior validation
   - Policy impact studies
   - Academic collaborations

### Getting Started

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Write tests** for new functionality
5. **Ensure tests pass**: `pytest` (backend) and `npm test` (frontend)
6. **Commit your changes**: `git commit -m 'Add amazing feature'`
7. **Push to branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for frontend code
- Write meaningful commit messages
- Add tests for new features
- Update documentation
- Keep PRs focused and small

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions

---

## 🛡️ Safety & Ethics

### Responsible AI Principles

1. **Transparency**
   - All outputs labeled as simulated projections
   - Clear distinction between predictions and possibilities
   - Open-source algorithms and methodologies

2. **Explainability**
   - Every decision traceable to source
   - LLM rationales provided
   - Confidence intervals on all metrics

3. **Human Oversight**
   - Human review required for policy decisions
   - Override mechanisms for agent actions
   - Validation against historical data

4. **Privacy Protection**
   - Anonymized demographic data
   - No personally identifiable information
   - Secure handling of sensitive municipal data

5. **Equity & Fairness**
   - Explicit equity metrics tracked
   - Bias detection in agent behaviors
   - Diverse stakeholder representation

6. **Limitations**
   - Clear documentation of model limitations
   - Uncertainty quantification
   - Validation requirements

### Disclaimer

**CityLab AI is a simulation tool for research and planning purposes.** All outputs should be:
- Validated against real-world data
- Reviewed by domain experts
- Used as one input among many in decision-making
- Not treated as definitive predictions

The developers are not responsible for decisions made based solely on simulation outputs.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 CityLab AI Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 💬 Support

### Getting Help

- **Documentation**: Check this README and [DEPLOYMENT.md](DEPLOYMENT.md)
- **GitHub Issues**: [Report bugs or request features](https://github.com/fanisridhar/CityLab-AI---Autonomous-Urban-Policy-Sandbox/issues)
- **Discussions**: [Join community discussions](https://github.com/fanisridhar/CityLab-AI---Autonomous-Urban-Policy-Sandbox/discussions)

### Community

- **GitHub**: [CityLab AI Repository](https://github.com/fanisridhar/CityLab-AI---Autonomous-Urban-Policy-Sandbox)
- **Issues**: [Bug Reports & Feature Requests](https://github.com/fanisridhar/CityLab-AI---Autonomous-Urban-Policy-Sandbox/issues)

### Citation

If you use CityLab AI in your research, please cite:

```bibtex
@software{citylab_ai_2024,
  title = {CityLab AI: Autonomous Urban Policy Sandbox},
  author = {CityLab AI Contributors},
  year = {2024},
  url = {https://github.com/fanisridhar/CityLab-AI---Autonomous-Urban-Policy-Sandbox},
  license = {MIT}
}
```

---

## 🙏 Acknowledgments

- **OpenStreetMap** for open geospatial data
- **LangChain** and **LlamaIndex** for LLM orchestration frameworks
- **Mesa** for agent-based modeling framework
- **FastAPI** and **Next.js** communities
- All contributors and supporters of this project

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/fanisridhar/CityLab-AI---Autonomous-Urban-Policy-Sandbox?style=social)
![GitHub forks](https://img.shields.io/github/forks/fanisridhar/CityLab-AI---Autonomous-Urban-Policy-Sandbox?style=social)
![GitHub issues](https://img.shields.io/github/issues/fanisridhar/CityLab-AI---Autonomous-Urban-Policy-Sandbox)
![GitHub pull requests](https://img.shields.io/github/issues-pr/fanisridhar/CityLab-AI---Autonomous-Urban-Policy-Sandbox)

---

<div align="center">

**Built with ❤️ for better cities**

[⬆ Back to Top](#-
