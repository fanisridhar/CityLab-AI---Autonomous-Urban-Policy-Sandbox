"""
Planner agent - proposes policies and reads regulations
"""
from typing import Dict, List, Optional, Any
from app.agents.base import BaseAgent
import structlog

logger = structlog.get_logger()


class PlannerAgent(BaseAgent):
    """Planner agent that proposes policies and consults regulations"""
    
    def __init__(self, agent_id: str, persona_config: Dict[str, Any], **kwargs):
        super().__init__(agent_id, "planner", persona_config, **kwargs)
        
        # Planner-specific state
        self.state.update({
            "proposed_policies": [],
            "budget_constraints": persona_config.get("budget_constraints", {}),
            "regulatory_knowledge": persona_config.get("regulatory_knowledge", []),
            "evaluation_criteria": persona_config.get("evaluation_criteria", [
                "equity", "efficiency", "sustainability", "cost"
            ])
        })
    
    def _get_system_prompt(self) -> str:
        return """You are an urban planner agent responsible for proposing and evaluating policies. Your role:
        - Consult relevant regulations, budgets, and case studies
        - Propose policies that balance multiple objectives (equity, efficiency, sustainability)
        - Evaluate policy impacts based on simulation results
        - Provide evidence-based recommendations with citations
        
        Always reference specific documents and regulations when making proposals."""
    
    def _build_reasoning_prompt(self, perception: Dict, retrieved_docs: Optional[List] = None) -> str:
        city_state = perception.get("city_state", {})
        current_metrics = city_state.get("metrics", {})
        
        prompt = f"""Current city metrics:
- Average commute time: {current_metrics.get('avg_commute_time', 'N/A')} minutes
- Transit modal share: {current_metrics.get('transit_modal_share', 'N/A')}
- Service coverage: {current_metrics.get('service_coverage', 'N/A')}
- Equity index: {current_metrics.get('equity_index', 'N/A')}

Budget constraints:
{self.state.get('budget_constraints', {})}

"""
        
        if retrieved_docs:
            prompt += "\nRelevant regulations and case studies:\n"
            for i, doc in enumerate(retrieved_docs[:5], 1):
                prompt += f"{i}. {doc.get('title', 'Document')}\n"
                prompt += f"   Type: {doc.get('document_type', 'unknown')}\n"
                prompt += f"   Content: {doc.get('content', '')[:300]}...\n\n"
        
        prompt += "\nBased on the current state and regulations, what policy should you propose? Provide specific recommendations with citations."
        
        return prompt
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response for planner actions"""
        action_type = "propose_policy"
        action_data = {
            "policy_type": "general",
            "policy_description": response,
            "estimated_cost": None,
            "expected_impact": {}
        }
        
        # Extract policy type from response
        response_lower = response.lower()
        if "congestion" in response_lower or "pricing" in response_lower:
            action_data["policy_type"] = "congestion_pricing"
        elif "bus" in response_lower or "transit" in response_lower:
            action_data["policy_type"] = "transit_improvement"
        elif "zoning" in response_lower:
            action_data["policy_type"] = "zoning_change"
        elif "bike" in response_lower or "cycling" in response_lower:
            action_data["policy_type"] = "bike_infrastructure"
        
        return {
            "action_type": action_type,
            "action_data": action_data,
            "rationale": response,
            "confidence": 0.8
        }
    
    def _update_state_from_action(self, action: Dict[str, Any]):
        """Update planner state after action"""
        if action.get("action_type") == "propose_policy":
            proposed_policies = self.state.get("proposed_policies", [])
            proposed_policies.append({
                "action_data": action.get("action_data"),
                "timestamp": action.get("timestamp")
            })
            self.state["proposed_policies"] = proposed_policies
