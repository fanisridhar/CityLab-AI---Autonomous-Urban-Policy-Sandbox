"""
Resident agent - represents citizens with schedules and mode choice
"""
from typing import Dict, List, Optional, Any
from app.agents.base import BaseAgent
import structlog

logger = structlog.get_logger()


class ResidentAgent(BaseAgent):
    """Resident agent with household schedules and transportation choices"""
    
    def __init__(self, agent_id: str, persona_config: Dict[str, Any], **kwargs):
        super().__init__(agent_id, "resident", persona_config, **kwargs)
        
        # Resident-specific state
        self.state.update({
            "home_location": persona_config.get("home_location"),
            "work_location": persona_config.get("work_location"),
            "schedule": persona_config.get("schedule", {}),  # Daily schedule
            "current_mode": persona_config.get("preferred_mode", "transit"),  # car, transit, bike, walk
            "current_location": persona_config.get("home_location"),
            "current_activity": "home",
            "commute_time": 0,
            "satisfaction": 0.7
        })
    
    def _get_system_prompt(self) -> str:
        return """You are a resident agent in an urban simulation. You have a daily schedule with activities 
        (home, work, shopping, etc.) and need to choose transportation modes. Consider factors like:
        - Cost (transit fare, parking, gas)
        - Time (commute duration)
        - Convenience and reliability
        - Environmental impact (if you care about it)
        - Current infrastructure (bus routes, bike lanes, congestion)
        
        Respond with your reasoning and proposed action in a clear format."""
    
    def _build_reasoning_prompt(self, perception: Dict, retrieved_docs: Optional[List] = None) -> str:
        current_time = perception.get("timestamp", {}).get("hour", 9)
        current_activity = self.state.get("current_activity", "home")
        schedule = self.state.get("schedule", {})
        
        # Determine next activity based on schedule
        next_activity = self._get_next_activity(current_time, schedule)
        
        prompt = f"""Current situation:
- Time: {current_time}:00
- Current activity: {current_activity}
- Current location: {self.state.get('current_location')}
- Next activity: {next_activity}
- Preferred mode: {self.state.get('current_mode')}
- Current commute time: {self.state.get('commute_time')} minutes
- Satisfaction: {self.state.get('satisfaction')}

City state:
- Transit delays: {perception.get('city_state', {}).get('transit_delays', 0)} minutes
- Traffic congestion: {perception.get('city_state', {}).get('traffic_level', 'normal')}
- Available transit routes: {perception.get('city_state', {}).get('transit_routes', [])}

"""
        
        if retrieved_docs:
            prompt += "\nRelevant policy documents:\n"
            for doc in retrieved_docs[:3]:  # Top 3 docs
                prompt += f"- {doc.get('title', 'Document')}: {doc.get('content', '')[:200]}...\n"
        
        prompt += "\nWhat should you do? Consider your schedule, transportation options, and any policy changes."
        
        return prompt
    
    def _get_next_activity(self, current_hour: int, schedule: Dict) -> str:
        """Determine next activity based on schedule"""
        # Simple schedule logic
        if 6 <= current_hour < 9:
            return "work"
        elif 9 <= current_hour < 17:
            return "work"
        elif 17 <= current_hour < 20:
            return "home"
        else:
            return "home"
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response for resident actions"""
        # Extract action type and data from response
        action_type = "move"
        action_data = {
            "destination": self.state.get("work_location") if self.state.get("current_activity") == "home" else self.state.get("home_location"),
            "mode": self.state.get("current_mode")
        }
        
        # Try to extract mode choice from response
        response_lower = response.lower()
        if "transit" in response_lower or "bus" in response_lower:
            action_data["mode"] = "transit"
        elif "car" in response_lower or "drive" in response_lower:
            action_data["mode"] = "car"
        elif "bike" in response_lower or "cycling" in response_lower:
            action_data["mode"] = "bike"
        elif "walk" in response_lower:
            action_data["mode"] = "walk"
        
        return {
            "action_type": action_type,
            "action_data": action_data,
            "rationale": response,
            "confidence": 0.7
        }
    
    def _update_state_from_action(self, action: Dict[str, Any]):
        """Update resident state after action"""
        action_data = action.get("action_data", {})
        if "destination" in action_data:
            self.state["current_location"] = action_data["destination"]
        if "mode" in action_data:
            self.state["current_mode"] = action_data["mode"]
        
        # Update activity based on location
        if self.state["current_location"] == self.state.get("home_location"):
            self.state["current_activity"] = "home"
        elif self.state["current_location"] == self.state.get("work_location"):
            self.state["current_activity"] = "work"
