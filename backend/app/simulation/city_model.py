"""
Mesa-based city model for agent-based simulation
"""
from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import NetworkGrid
import networkx as nx
from typing import Dict, List, Any, Optional
import structlog

from app.agents import ResidentAgent, TransitOperatorAgent, PlannerAgent, OrchestratorAgent

logger = structlog.get_logger()


class CityModel(Model):
    """Mesa model for city simulation"""
    
    def __init__(
        self,
        city_data: Dict[str, Any],
        scenario_config: Dict[str, Any],
        agents_config: List[Dict[str, Any]],
        seed: Optional[int] = None
    ):
        super().__init__(seed=seed)
        
        self.city_data = city_data
        self.scenario_config = scenario_config
        self.schedule = SimultaneousActivation(self)
        
        # Create network graph from city data
        self.graph = self._create_network_graph(city_data)
        self.grid = NetworkGrid(self.graph)
        
        # City state
        self.city_state = {
            "transit_routes": city_data.get("transit_routes", []),
            "transit_delays": {},
            "traffic_level": "normal",
            "transit_ridership": {},
            "demand_changes": {},
            "service_coverage": 0.7,
            "metrics": {}
        }
        
        # Initialize agents
        self.agents = {}
        self._initialize_agents(agents_config)
        
        # Simulation state
        self.current_tick = 0
        self.simulation_time = None  # Will be datetime object
        
        logger.info("CityModel initialized", agents_count=len(self.agents))
    
    def _create_network_graph(self, city_data: Dict) -> nx.Graph:
        """Create network graph from city data"""
        G = nx.Graph()
        
        # Add nodes (intersections, POIs)
        nodes = city_data.get("nodes", [])
        for node in nodes:
            G.add_node(node["id"], **node.get("attributes", {}))
        
        # Add edges (streets)
        edges = city_data.get("edges", [])
        for edge in edges:
            G.add_edge(
                edge["source"],
                edge["target"],
                weight=edge.get("weight", 1.0),
                **edge.get("attributes", {})
            )
        
        return G
    
    def _initialize_agents(self, agents_config: List[Dict]):
        """Initialize agents from configuration"""
        for agent_config in agents_config:
            agent_type = agent_config.get("agent_type")
            agent_id = agent_config.get("agent_id", f"{agent_type}_{len(self.agents)}")
            
            if agent_type == "resident":
                agent = ResidentAgent(agent_id, agent_config.get("persona_config", {}))
            elif agent_type == "transit_operator":
                agent = TransitOperatorAgent(agent_id, agent_config.get("persona_config", {}))
            elif agent_type == "planner":
                agent = PlannerAgent(agent_id, agent_config.get("persona_config", {}))
            elif agent_type == "orchestrator":
                agent = OrchestratorAgent(agent_id, agent_config.get("persona_config", {}))
            else:
                logger.warning("Unknown agent type", agent_type=agent_type)
                continue
            
            self.agents[agent_id] = agent
            self.schedule.add(agent)
            
            # Place agent on grid if location specified
            location = agent.state.get("location") or agent.state.get("home_location")
            if location and location in self.graph.nodes():
                self.grid.place_agent(agent, location)
    
    def step(self):
        """Execute one simulation step"""
        # Get environment state for agents
        environment_state = {
            "timestamp": {
                "tick": self.current_tick,
                "hour": (self.current_tick // 60) % 24,  # Assuming 1 tick = 1 minute
                "day": self.current_tick // (60 * 24)
            },
            "city_state": self.city_state,
            "agents": [{"id": aid, "state": agent.state} for aid, agent in self.agents.items()],
            "events": []
        }
        
        # Execute agent steps
        agent_actions = {}
        for agent_id, agent in self.agents.items():
            try:
                # TODO: Retrieve relevant docs via RAG
                retrieved_docs = []
                action = agent.step(environment_state, retrieved_docs)
                agent_actions[agent_id] = action
            except Exception as e:
                logger.error("Agent step failed", agent_id=agent_id, error=str(e))
                agent_actions[agent_id] = {"action_type": "error", "action_data": {}}
        
        # Update city state based on agent actions
        self._update_city_state(agent_actions)
        
        # Update metrics
        agent_states = [agent.state for agent in self.agents.values()]
        if "orchestrator" in [a.agent_type for a in self.agents.values()]:
            orchestrator = next(a for a in self.agents.values() if a.agent_type == "orchestrator")
            self.city_state["metrics"] = orchestrator.aggregate_kpis(agent_states, self.city_state)
        
        self.current_tick += 1
        self.schedule.step()
    
    def _update_city_state(self, agent_actions: Dict[str, Dict]):
        """Update city state based on agent actions"""
        # Update transit ridership from resident actions
        transit_ridership = {}
        for agent_id, action in agent_actions.items():
            if action.get("action_type") == "move":
                mode = action.get("action_data", {}).get("mode")
                if mode == "transit":
                    route_id = action.get("action_data", {}).get("route_id", "default")
                    transit_ridership[route_id] = transit_ridership.get(route_id, 0) + 1
        
        self.city_state["transit_ridership"] = transit_ridership
        
        # Update transit frequencies from transit operator actions
        for agent_id, action in agent_actions.items():
            if action.get("action_type") == "adjust_frequency":
                route_id = action.get("action_data", {}).get("route_id")
                new_freq = action.get("action_data", {}).get("new_frequency")
                if route_id and new_freq:
                    # Update in city state
                    if "transit_frequencies" not in self.city_state:
                        self.city_state["transit_frequencies"] = {}
                    self.city_state["transit_frequencies"][route_id] = new_freq
    
    def get_state_snapshot(self) -> Dict[str, Any]:
        """Get current simulation state snapshot"""
        return {
            "tick": self.current_tick,
            "simulation_time": self.simulation_time,
            "agent_states": {aid: agent.state for aid, agent in self.agents.items()},
            "city_state": self.city_state.copy(),
            "events": []
        }
