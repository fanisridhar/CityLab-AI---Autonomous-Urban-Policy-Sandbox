"""
Simulation state and metrics models
"""
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class SimulationState(Base):
    """Snapshot of simulation state at a given tick"""
    __tablename__ = "simulation_states"
    
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("scenario_runs.id"), nullable=False)
    tick = Column(Integer, nullable=False, index=True)
    simulation_time = Column(DateTime(timezone=True))  # Simulated datetime
    
    # State data
    agent_states = Column(JSON)  # All agent positions/states
    city_state = Column(JSON)  # Infrastructure, traffic, etc.
    events = Column(JSON)  # Events that occurred this tick
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    run = relationship("ScenarioRun", back_populates="simulation_states")


class SimulationMetrics(Base):
    """Aggregated metrics for a simulation run"""
    __tablename__ = "simulation_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("scenario_runs.id"), nullable=False, unique=True)
    
    # Policy impact metrics
    avg_commute_time = Column(Float)  # minutes
    commute_time_change_pct = Column(Float)  # % change from baseline
    transit_modal_share = Column(Float)  # 0-1
    transit_ridership = Column(Integer)
    emissions_proxy = Column(Float)  # CO2 equivalent
    service_coverage = Column(Float)  # 0-1
    
    # Equity metrics
    job_access_30min = Column(Float)  # % of residents with job access within 30 min
    equity_index = Column(Float)  # Composite equity score
    
    # Additional metrics
    metrics_json = Column(JSON)  # Flexible additional metrics
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    run = relationship("ScenarioRun", uselist=False)
