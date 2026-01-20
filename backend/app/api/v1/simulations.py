"""
Simulation API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.models.simulation import SimulationState, SimulationMetrics
from app.models.scenario import ScenarioRun

router = APIRouter()


class SimulationStateResponse(BaseModel):
    id: int
    run_id: int
    tick: int
    simulation_time: Optional[datetime]
    agent_states: Optional[dict]
    city_state: Optional[dict]
    events: Optional[dict]
    timestamp: datetime
    
    class Config:
        from_attributes = True


class SimulationMetricsResponse(BaseModel):
    id: int
    run_id: int
    avg_commute_time: Optional[float]
    commute_time_change_pct: Optional[float]
    transit_modal_share: Optional[float]
    transit_ridership: Optional[int]
    emissions_proxy: Optional[float]
    service_coverage: Optional[float]
    job_access_30min: Optional[float]
    equity_index: Optional[float]
    metrics_json: Optional[dict]
    
    class Config:
        from_attributes = True


@router.get("/runs/{run_id}/states", response_model=List[SimulationStateResponse])
async def get_simulation_states(
    run_id: int,
    tick_start: Optional[int] = None,
    tick_end: Optional[int] = None,
    limit: int = 1000,
    db: Session = Depends(get_db)
):
    """Get simulation states for a run"""
    # Verify run exists
    run = db.query(ScenarioRun).filter(ScenarioRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Scenario run not found")
    
    query = db.query(SimulationState).filter(SimulationState.run_id == run_id)
    
    if tick_start is not None:
        query = query.filter(SimulationState.tick >= tick_start)
    if tick_end is not None:
        query = query.filter(SimulationState.tick <= tick_end)
    
    states = query.order_by(SimulationState.tick).limit(limit).all()
    return states


@router.get("/runs/{run_id}/states/{tick}", response_model=SimulationStateResponse)
async def get_simulation_state_at_tick(
    run_id: int,
    tick: int,
    db: Session = Depends(get_db)
):
    """Get simulation state at a specific tick"""
    state = db.query(SimulationState).filter(
        SimulationState.run_id == run_id,
        SimulationState.tick == tick
    ).first()
    
    if not state:
        raise HTTPException(status_code=404, detail="Simulation state not found")
    
    return state


@router.get("/runs/{run_id}/metrics", response_model=SimulationMetricsResponse)
async def get_simulation_metrics(
    run_id: int,
    db: Session = Depends(get_db)
):
    """Get aggregated metrics for a simulation run"""
    metrics = db.query(SimulationMetrics).filter(
        SimulationMetrics.run_id == run_id
    ).first()
    
    if not metrics:
        raise HTTPException(status_code=404, detail="Simulation metrics not found")
    
    return metrics
