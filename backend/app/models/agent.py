"""
Agent database models
"""
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Float, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class AgentType(enum.Enum):
    """Agent type enumeration"""
    RESIDENT = "resident"
    TRANSIT_OPERATOR = "transit_operator"
    PLANNER = "planner"
    DEVELOPER = "developer"
    BUSINESS = "business"
    EMERGENCY_SERVICE = "emergency_service"
    ORCHESTRATOR = "orchestrator"


class Agent(Base):
    """Agent model"""
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_type = Column(Enum(AgentType), nullable=False, index=True)
    name = Column(String(255))
    persona_config = Column(JSON)  # Agent-specific configuration
    location = Column(JSON)  # Geographic location
    state = Column(JSON)  # Current agent state
    memory_store_id = Column(String(255))  # Reference to vector DB memory
    
    # Relationships
    actions = relationship("AgentAction", back_populates="agent", cascade="all, delete-orphan")


class AgentAction(Base):
    """Agent action with explainability"""
    __tablename__ = "agent_actions"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    simulation_tick = Column(Integer, nullable=False)
    action_type = Column(String(100))  # e.g., "move", "change_route", "propose_policy"
    action_data = Column(JSON)  # Action parameters
    
    # Explainability
    rationale = Column(Text)  # LLM-generated explanation
    retrieved_docs = Column(JSON)  # Policy documents consulted
    prompt_used = Column(Text)  # Prompt that generated this action
    confidence_score = Column(Float)
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    agent = relationship("Agent", back_populates="actions")
