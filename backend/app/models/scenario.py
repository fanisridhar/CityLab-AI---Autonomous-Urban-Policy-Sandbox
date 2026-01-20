"""
Scenario database models
"""
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Scenario(Base):
    """Scenario model for policy experiments"""
    __tablename__ = "scenarios"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    policy_type = Column(String(100))  # e.g., "congestion_pricing", "bus_priority", "zoning"
    policy_config = Column(JSON)  # Policy parameters
    city_data_id = Column(Integer, ForeignKey("city_data.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String(100))
    
    # Relationships
    city_data = relationship("CityData", back_populates="scenarios")
    runs = relationship("ScenarioRun", back_populates="scenario", cascade="all, delete-orphan")


class ScenarioRun(Base):
    """Individual simulation run for a scenario"""
    __tablename__ = "scenario_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=False)
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    simulation_days = Column(Integer, default=7)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True))
    seed = Column(Integer)  # Random seed for reproducibility
    
    # Results
    metrics = Column(JSON)  # Aggregated KPIs
    error_message = Column(Text)
    
    # Relationships
    scenario = relationship("Scenario", back_populates="runs")
    simulation_states = relationship("SimulationState", back_populates="run", cascade="all, delete-orphan")
