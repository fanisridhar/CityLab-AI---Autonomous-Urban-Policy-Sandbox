"""
Orchestrator agent - coordinates simulation and aggregates KPIs
"""
from typing import Dict, List, Optional, Any
from app.agents.base import BaseAgent
import structlog

logger = structlog.get_logger()


class OrchestratorAgent(BaseAgent):
    """Orchestrator agent that coordinates simulation and manages scenarios"""
    
    def __init__(self, agent_id: str, persona_config: Dict[str, Any], **kwargs):
        super().__init__(agent_id, "orchestrator", persona_config, **kwargs)
        
        # Orchestrator-specific state
        self.state.update({
            "current_tick": 0,
            "simulation_days": 7,
            "scenario_config": persona_config.get("scenario_config", {}),
            "kpis": {},
            "safety_constraints": persona_config.get("safety_constraints", {})
        })
    
    def _get_system_prompt(self) -> str:
        return """You are the orchestrator agent managing the urban simulation. Your responsibilities:
        - Coordinate simulation ticks and manage time progression
        - Aggregate KPIs from all agents and city state
        - Enforce safety constraints and validate actions
        - Manage scenario rollout and policy deployment
        - Generate summary reports with explainable outcomes"""
    
    def _build_reasoning_prompt(self, perception: Dict, retrieved_docs: Optional[List] = None) -> str:
        current_tick = self.state.get("current_tick", 0)
        scenario_config = self.state.get("scenario_config", {})
        
        prompt = f"""Simulation state:
- Current tick: {current_tick}
- Simulation days: {self.state.get('simulation_days', 7)}
- Scenario: {scenario_config.get('name', 'default')}
- Policy: {scenario_config.get('policy_type', 'none')}

Current KPIs:
{self.state.get('kpis', {})}

Safety constraints:
{self.state.get('safety_constraints', {})}

"""
        
        prompt += "\nWhat should happen in the next simulation tick? Coordinate agent actions and update metrics."
        
        return prompt
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response for orchestrator actions"""
        return {
            "action_type": "tick",
            "action_data": {
                "next_tick": self.state.get("current_tick", 0) + 1,
                "instructions": response
            },
            "rationale": response,
            "confidence": 0.9
        }
    
    def aggregate_kpis(self, agent_states: List[Dict], city_state: Dict) -> Dict[str, Any]:
        """Aggregate KPIs from agent states and city state"""
        # Calculate aggregate metrics
        kpis = {
            "avg_commute_time": city_state.get("avg_commute_time", 0),
            "transit_ridership": city_state.get("transit_ridership", 0),
            "transit_modal_share": city_state.get("transit_modal_share", 0),
            "service_coverage": city_state.get("service_coverage", 0),
            "equity_index": city_state.get("equity_index", 0.7),
            "emissions_proxy": city_state.get("emissions_proxy", 0)
        }
        
        self.state["kpis"] = kpis
        return kpis
