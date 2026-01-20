"""
Agent API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.models.agent import Agent, AgentAction, AgentType

router = APIRouter()


class AgentResponse(BaseModel):
    id: int
    agent_type: str
    name: Optional[str]
    persona_config: Optional[dict]
    location: Optional[dict]
    state: Optional[dict]
    
    class Config:
        from_attributes = True


class AgentActionResponse(BaseModel):
    id: int
    agent_id: int
    simulation_tick: int
    action_type: str
    action_data: Optional[dict]
    rationale: Optional[str]
    retrieved_docs: Optional[dict]
    confidence_score: Optional[float]
    timestamp: datetime
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[AgentResponse])
async def list_agents(
    agent_type: Optional[AgentType] = Query(None),
    run_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List agents, optionally filtered by type or run"""
    query = db.query(Agent)
    
    if agent_type:
        query = query.filter(Agent.agent_type == agent_type)
    
    # TODO: Filter by run_id when agent-run relationship is established
    agents = query.all()
    return agents


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.get("/{agent_id}/actions", response_model=List[AgentActionResponse])
async def get_agent_actions(
    agent_id: int,
    tick_start: Optional[int] = Query(None),
    tick_end: Optional[int] = Query(None),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    """Get actions for a specific agent"""
    query = db.query(AgentAction).filter(AgentAction.agent_id == agent_id)
    
    if tick_start is not None:
        query = query.filter(AgentAction.simulation_tick >= tick_start)
    if tick_end is not None:
        query = query.filter(AgentAction.simulation_tick <= tick_end)
    
    actions = query.order_by(AgentAction.simulation_tick).limit(limit).all()
    return actions
