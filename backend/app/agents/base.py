"""
Base agent class with LLM reasoning capabilities
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import structlog

from app.core.config import settings

logger = structlog.get_logger()


class BaseAgent(ABC):
    """Base class for all agents with LLM reasoning"""
    
    def __init__(
        self,
        agent_id: str,
        agent_type: str,
        persona_config: Dict[str, Any],
        llm_provider: str = "openai"
    ):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.persona_config = persona_config
        self.state: Dict[str, Any] = {}
        self.memory: List[Dict[str, Any]] = []
        
        # Initialize LLM
        if llm_provider == "openai" and settings.OPENAI_API_KEY:
            self.llm = ChatOpenAI(
                model="gpt-4-turbo-preview",
                temperature=0.7,
                api_key=settings.OPENAI_API_KEY
            )
        elif llm_provider == "anthropic" and settings.ANTHROPIC_API_KEY:
            self.llm = ChatAnthropic(
                model="claude-3-opus-20240229",
                temperature=0.7,
                api_key=settings.ANTHROPIC_API_KEY
            )
        else:
            logger.warning("No LLM API key found, using mock LLM")
            self.llm = None
    
    def perceive(self, environment_state: Dict[str, Any]) -> Dict[str, Any]:
        """Perceive the current environment state"""
        perception = {
            "timestamp": environment_state.get("timestamp"),
            "location": self.state.get("location"),
            "nearby_agents": environment_state.get("agents", []),
            "city_state": environment_state.get("city_state", {}),
            "events": environment_state.get("events", [])
        }
        return perception
    
    def reason(
        self,
        perception: Dict[str, Any],
        retrieved_docs: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Use LLM to reason about the current situation"""
        if not self.llm:
            # Fallback to simple rule-based reasoning
            return self._simple_reason(perception)
        
        # Build prompt with context
        prompt = self._build_reasoning_prompt(perception, retrieved_docs)
        
        try:
            messages = [
                SystemMessage(content=self._get_system_prompt()),
                HumanMessage(content=prompt)
            ]
            response = self.llm.invoke(messages)
            reasoning = self._parse_llm_response(response.content)
            reasoning["retrieved_docs"] = retrieved_docs
            reasoning["prompt_used"] = prompt
            return reasoning
        except Exception as e:
            logger.error("LLM reasoning failed", error=str(e), agent_id=self.agent_id)
            return self._simple_reason(perception)
    
    def act(self, reasoning: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action based on reasoning"""
        action = {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "action_type": reasoning.get("action_type", "wait"),
            "action_data": reasoning.get("action_data", {}),
            "rationale": reasoning.get("rationale", ""),
            "confidence": reasoning.get("confidence", 0.5)
        }
        
        # Update agent state based on action
        self._update_state_from_action(action)
        
        return action
    
    def step(self, environment_state: Dict[str, Any], retrieved_docs: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Complete agent step: perceive -> reason -> act"""
        perception = self.perceive(environment_state)
        reasoning = self.reason(perception, retrieved_docs)
        action = self.act(reasoning)
        
        # Store in memory
        self.memory.append({
            "perception": perception,
            "reasoning": reasoning,
            "action": action
        })
        
        return action
    
    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Get system prompt for this agent type"""
        pass
    
    @abstractmethod
    def _build_reasoning_prompt(self, perception: Dict, retrieved_docs: Optional[List]) -> str:
        """Build reasoning prompt from perception"""
        pass
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured reasoning"""
        # Simple parsing - can be enhanced with structured output
        return {
            "action_type": "wait",  # Default
            "action_data": {},
            "rationale": response,
            "confidence": 0.7
        }
    
    def _simple_reason(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback simple reasoning without LLM"""
        return {
            "action_type": "wait",
            "action_data": {},
            "rationale": "Simple rule-based reasoning",
            "confidence": 0.5
        }
    
    def _update_state_from_action(self, action: Dict[str, Any]):
        """Update agent state based on executed action"""
        # Override in subclasses
        pass
