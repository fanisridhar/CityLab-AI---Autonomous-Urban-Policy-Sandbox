"""
Transit operator agent - manages routes and frequencies
"""
from typing import Dict, List, Optional, Any
from app.agents.base import BaseAgent
import structlog

logger = structlog.get_logger()


class TransitOperatorAgent(BaseAgent):
    """Transit operator agent that adjusts routes and frequencies"""
    
    def __init__(self, agent_id: str, persona_config: Dict[str, Any], **kwargs):
        super().__init__(agent_id, "transit_operator", persona_config, **kwargs)
        
        # Transit-specific state
        self.state.update({
            "routes": persona_config.get("routes", []),
            "frequencies": persona_config.get("frequencies", {}),  # route_id -> frequency (minutes)
            "budget": persona_config.get("budget", 1000000),
            "ridership": persona_config.get("ridership", {}),  # route_id -> daily_ridership
            "operating_costs": persona_config.get("operating_costs", {}),
            "satisfaction_score": 0.7
        })
    
    def _get_system_prompt(self) -> str:
        return """You are a transit operator agent managing public transportation in a city. Your goals are:
        - Maximize ridership and service coverage
        - Maintain financial sustainability within budget constraints
        - Respond to changes in demand and infrastructure
        - Consider equity and accessibility
        
        You can adjust route frequencies, add/remove routes, and reallocate resources.
        Consider policy documents, budget constraints, and current ridership data."""
    
    def _build_reasoning_prompt(self, perception: Dict, retrieved_docs: Optional[List] = None) -> str:
        city_state = perception.get("city_state", {})
        current_ridership = city_state.get("transit_ridership", {})
        demand_changes = city_state.get("demand_changes", {})
        
        prompt = f"""Current transit system state:
- Routes: {len(self.state.get('routes', []))}
- Current ridership: {current_ridership}
- Budget: ${self.state.get('budget', 0):,}
- Operating costs: ${sum(self.state.get('operating_costs', {}).values()):,}
- Demand changes: {demand_changes}
- Service coverage: {city_state.get('service_coverage', 0.7)}

Current route frequencies:
{self.state.get('frequencies', {})}

"""
        
        if retrieved_docs:
            prompt += "\nRelevant policy/budget documents:\n"
            for doc in retrieved_docs[:3]:
                prompt += f"- {doc.get('title', 'Document')}: {doc.get('content', '')[:200]}...\n"
        
        prompt += "\nWhat adjustments should you make to routes or frequencies? Consider budget, demand, and policy constraints."
        
        return prompt
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response for transit operator actions"""
        action_type = "adjust_frequency"
        action_data = {
            "route_id": None,
            "new_frequency": None
        }
        
        # Simple extraction - can be enhanced
        response_lower = response.lower()
        
        # Try to extract route and frequency information
        # This is simplified - in production, use structured output
        if "increase" in response_lower or "more frequent" in response_lower:
            # Default action: increase frequency on most popular route
            routes = self.state.get("routes", [])
            if routes:
                ridership = self.state.get("ridership", {})
                if ridership:
                    most_popular = max(ridership.items(), key=lambda x: x[1])
                    action_data["route_id"] = most_popular[0]
                    current_freq = self.state.get("frequencies", {}).get(most_popular[0], 15)
                    action_data["new_frequency"] = max(5, current_freq - 2)  # Increase frequency
        
        return {
            "action_type": action_type,
            "action_data": action_data,
            "rationale": response,
            "confidence": 0.7
        }
    
    def _update_state_from_action(self, action: Dict[str, Any]):
        """Update transit operator state after action"""
        action_data = action.get("action_data", {})
        if action.get("action_type") == "adjust_frequency":
            route_id = action_data.get("route_id")
            new_freq = action_data.get("new_frequency")
            if route_id and new_freq:
                frequencies = self.state.get("frequencies", {})
                frequencies[route_id] = new_freq
                self.state["frequencies"] = frequencies
