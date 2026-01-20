"""
Explainability API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.models.agent import AgentAction

router = APIRouter()


class ExplainabilityResponse(BaseModel):
    action_id: int
    agent_id: int
    action_type: str
    rationale: Optional[str]
    retrieved_docs: Optional[dict]
    prompt_used: Optional[str]
    confidence_score: Optional[float]
    
    class Config:
        from_attributes = True


@router.get("/actions/{action_id}", response_model=ExplainabilityResponse)
async def get_action_explanation(
    action_id: int,
    db: Session = Depends(get_db)
):
    """Get explainability data for a specific action"""
    action = db.query(AgentAction).filter(AgentAction.id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    
    return action


@router.get("/agents/{agent_id}/explanations", response_model=List[ExplainabilityResponse])
async def get_agent_explanations(
    agent_id: int,
    tick_start: Optional[int] = None,
    tick_end: Optional[int] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get explanations for all actions by an agent"""
    query = db.query(AgentAction).filter(AgentAction.agent_id == agent_id)
    
    if tick_start is not None:
        query = query.filter(AgentAction.simulation_tick >= tick_start)
    if tick_end is not None:
        query = query.filter(AgentAction.simulation_tick <= tick_end)
    
    actions = query.order_by(AgentAction.simulation_tick.desc()).limit(limit).all()
    return actions
