"""
Scenario API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.models.scenario import Scenario, ScenarioRun
from app.models.simulation import SimulationMetrics

router = APIRouter()


class ScenarioCreate(BaseModel):
    name: str
    description: Optional[str] = None
    policy_type: str
    policy_config: dict
    city_data_id: Optional[int] = None
    created_by: Optional[str] = None


class ScenarioResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    policy_type: Optional[str]
    policy_config: Optional[dict]
    city_data_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ScenarioRunCreate(BaseModel):
    simulation_days: int = 7
    seed: Optional[int] = None


class ScenarioRunResponse(BaseModel):
    id: int
    scenario_id: int
    status: str
    simulation_days: int
    start_time: datetime
    end_time: Optional[datetime]
    seed: Optional[int]
    metrics: Optional[dict]
    
    class Config:
        from_attributes = True


@router.post("/", response_model=ScenarioResponse, status_code=status.HTTP_201_CREATED)
async def create_scenario(
    scenario: ScenarioCreate,
    db: Session = Depends(get_db)
):
    """Create a new scenario"""
    db_scenario = Scenario(**scenario.dict())
    db.add(db_scenario)
    db.commit()
    db.refresh(db_scenario)
    return db_scenario


@router.get("/", response_model=List[ScenarioResponse])
async def list_scenarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all scenarios"""
    scenarios = db.query(Scenario).offset(skip).limit(limit).all()
    return scenarios


@router.get("/{scenario_id}", response_model=ScenarioResponse)
async def get_scenario(
    scenario_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific scenario"""
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario


@router.post("/{scenario_id}/runs", response_model=ScenarioRunResponse, status_code=status.HTTP_201_CREATED)
async def create_scenario_run(
    scenario_id: int,
    run_config: ScenarioRunCreate,
    db: Session = Depends(get_db)
):
    """Create and start a new scenario run"""
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    db_run = ScenarioRun(
        scenario_id=scenario_id,
        simulation_days=run_config.simulation_days,
        seed=run_config.seed,
        status="pending"
    )
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    
    # Trigger simulation task via Celery
    from app.tasks.simulation import run_simulation_task
    run_simulation_task.delay(db_run.id)
    
    return db_run


@router.get("/{scenario_id}/runs", response_model=List[ScenarioRunResponse])
async def list_scenario_runs(
    scenario_id: int,
    db: Session = Depends(get_db)
):
    """List all runs for a scenario"""
    runs = db.query(ScenarioRun).filter(ScenarioRun.scenario_id == scenario_id).all()
    return runs


@router.get("/{scenario_id}/runs/{run_id}", response_model=ScenarioRunResponse)
async def get_scenario_run(
    scenario_id: int,
    run_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific scenario run"""
    run = db.query(ScenarioRun).filter(
        ScenarioRun.id == run_id,
        ScenarioRun.scenario_id == scenario_id
    ).first()
    if not run:
        raise HTTPException(status_code=404, detail="Scenario run not found")
    return run
