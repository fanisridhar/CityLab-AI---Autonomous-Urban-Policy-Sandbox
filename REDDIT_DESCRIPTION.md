# CityLab AI — Autonomous Urban Policy Sandbox

## 🏙️ What is this?

**CityLab AI** is an open-source multi-agent urban simulator where LLM-driven stakeholder agents (residents, transit operators, planners, businesses, emergency services) test policies, infrastructure changes, and events in a sandboxed digital twin of a city. It produces explainable outcomes, tradeoffs, and actionable recommendations.

Think of it as **SimCity meets ChatGPT** — but for real urban planning decisions.

## 🚀 Why This is Mind-Blowing

### 1. **Real-World Data Integration**
- Import GIS maps, transit networks, population/POI datasets, traffic counts, and historical events
- Works with OpenStreetMap data out of the box
- Supports custom city data ingestion

### 2. **Multi-Agent Reasoning with LLMs**
- Uses LLMs (GPT-4, Claude) not just for chat, but as **cognitive controllers** for heterogeneous agents
- Agents interpret goals, read policy docs, negotiate, and generate structured actions
- Each agent has its own persona, memory, and decision-making process

### 3. **Scenario Experimentation**
- Run "what if?" experiments at city scale
- Test policies like congestion pricing, bus-priority lanes, zoning changes
- Human-in-the-loop validation for realistic outcomes

### 4. **Explainable AI**
- Every agent decision links back to evidence (policy docs, simulation traces, retrieved sources)
- LLM-generated rationales for each action
- Full provenance tracking

## 🏗️ Tech Stack

**Frontend:**
- Next.js 14 + TypeScript
- Mapbox/Deck.gl for interactive geospatial visualization
- Real-time dashboards with Recharts
- Tailwind CSS for modern UI

**Backend:**
- FastAPI (Python) for simulation control and API
- LangChain/LlamaIndex for agent orchestration and RAG
- Mesa for agent-based modeling
- Celery + Redis for background jobs
- PostgreSQL for scenario metadata and time series
- Chroma/Pinecone for vector storage (policy/document embeddings)

**Agents:**
- **Resident Agents**: Household schedules, mode choice (car/transit/bike), respond to price/infrastructure changes
- **Transit Operator**: Adjusts routes/frequencies, invests budget, reacts to ridership
- **Planner/Policy Agent**: Proposes rules, reads legislation via RAG, evaluates budget constraints
- **Developer/Business Agent**: Decides where to build/price services, reacts to zoning changes
- **Emergency Services**: Reacts to incidents, evaluates response times
- **Orchestrator**: Coordinates simulation ticks, manages scenario rollout, aggregates KPIs

## 📊 What You Can Do

### MVP Features (Current)
- Import street graphs and POIs from OpenStreetMap
- Resident agents with commuter schedules and route choice
- Transit operator agent that can change routes/frequencies
- Scenario runner: simulate N days, collect KPIs
- Interactive map visualization with time slider
- Explainability: agent actions annotated with prompts/retrieved docs

### Metrics Tracked
- Average commute time
- Transit modal share
- Transit ridership
- Service coverage
- Equity indices (access to jobs within 30 min)
- Emissions proxy
- Policy impact percentages

## 🎯 Use Cases

1. **Urban Planners**: Preview policy impacts before implementation
2. **Transit Agencies**: Test route changes and frequency adjustments
3. **City Governments**: Evaluate infrastructure investments
4. **Researchers**: Study urban dynamics and policy effectiveness
5. **Consultants**: Create evidence-based recommendations for clients
6. **NGOs**: Advocate for equitable transportation policies

## 🛡️ Safety & Ethics

- All outputs labeled as **simulated projections** (not predictions)
- Confidence ranges and provenance provided
- Human review required for real policy decisions
- Privacy protection for sensitive municipal data
- Rate limiting on automated actions

## 🚀 Getting Started

### Quick Start (Docker)
```bash
git clone https://github.com/fanisridhar/CityLab-AI---Autonomous-Urban-Policy-Sandbox.git
cd CityLab-AI---Autonomous-Urban-Policy-Sandbox
docker-compose up -d
```

### Manual Setup
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📈 Roadmap

- [ ] Enhanced agent behaviors (more realistic decision-making)
- [ ] Additional agent types (businesses, developers, emergency services)
- [ ] More policy types (zoning, parking, bike infrastructure)
- [ ] Historical data validation
- [ ] Multi-city support
- [ ] Collaborative scenario editing
- [ ] Export reports with citations
- [ ] API for programmatic access

## 🤝 Contributing

Contributions welcome! Areas where help is needed:
- Agent behavior improvements
- Additional data sources
- UI/UX enhancements
- Documentation
- Testing
- Performance optimization

## 📝 License

MIT License - see LICENSE file

## 🔗 Links

- **GitHub**: https://github.com/fanisridhar/CityLab-AI---Autonomous-Urban-Policy-Sandbox
- **Documentation**: See README.md and DEPLOYMENT.md
- **Issues**: https://github.com/fanisridhar/CityLab-AI---Autonomous-Urban-Policy-Sandbox/issues

## 💬 Discussion

This is an early-stage project, and we'd love your feedback! What features would be most valuable? What use cases should we prioritize? Let's build something that makes urban planning more data-driven and equitable.

---

**Built with ❤️ for better cities**
