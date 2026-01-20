"""
Simulation engine that orchestrates runs and manages state
"""
from typing import Dict, List, Any, Optional
import structlog
from datetime import datetime, timedelta

from app.simulation.city_model import CityModel
from app.core.database import SessionLocal
from app.models.scenario import ScenarioRun
from app.models.simulation import SimulationState, SimulationMetrics
from app.models.agent import Agent, AgentAction

logger = structlog.get_logger()


class SimulationEngine:
    """Engine for running simulations and persisting results"""
    
    def __init__(self, run_id: int):
        self.run_id = run_id
        self.db = SessionLocal()
        self.model: Optional[CityModel] = None
    
    def initialize(self, scenario_config: Dict, city_data: Dict, agents_config: List[Dict], seed: Optional[int] = None):
        """Initialize simulation model"""
        try:
            self.model = CityModel(
                city_data=city_data,
                scenario_config=scenario_config,
                agents_config=agents_config,
                seed=seed
            )
            
            # Update run status
            run = self.db.query(ScenarioRun).filter(ScenarioRun.id == self.run_id).first()
            if run:
                run.status = "running"
                self.db.commit()
            
            logger.info("Simulation initialized", run_id=self.run_id)
        except Exception as e:
            logger.error("Simulation initialization failed", error=str(e), run_id=self.run_id)
            raise
    
    def run(self, simulation_days: int = 7):
        """Run simulation for specified days"""
        if not self.model:
            raise ValueError("Simulation not initialized")
        
        ticks_per_day = 24 * 60  # 1 tick = 1 minute
        total_ticks = simulation_days * ticks_per_day
        
        logger.info("Starting simulation", run_id=self.run_id, total_ticks=total_ticks)
        
        # Initialize simulation time
        self.model.simulation_time = datetime.now().replace(hour=6, minute=0, second=0)
        
        try:
            for tick in range(total_ticks):
                # Execute simulation step
                self.model.step()
                
                # Update simulation time
                self.model.simulation_time += timedelta(minutes=1)
                
                # Save state snapshot periodically (every hour)
                if tick % 60 == 0:
                    self._save_state_snapshot()
                
                # Save agent actions
                self._save_agent_actions(tick)
            
            # Calculate and save final metrics
            self._save_final_metrics()
            
            # Update run status
            run = self.db.query(ScenarioRun).filter(ScenarioRun.id == self.run_id).first()
            if run:
                run.status = "completed"
                run.end_time = datetime.now()
                self.db.commit()
            
            logger.info("Simulation completed", run_id=self.run_id)
            
        except Exception as e:
            logger.error("Simulation failed", error=str(e), run_id=self.run_id)
            run = self.db.query(ScenarioRun).filter(ScenarioRun.id == self.run_id).first()
            if run:
                run.status = "failed"
                run.error_message = str(e)
                self.db.commit()
            raise
    
    def _save_state_snapshot(self):
        """Save simulation state snapshot to database"""
        if not self.model:
            return
        
        snapshot = self.model.get_state_snapshot()
        
        db_state = SimulationState(
            run_id=self.run_id,
            tick=snapshot["tick"],
            simulation_time=snapshot["simulation_time"],
            agent_states=snapshot["agent_states"],
            city_state=snapshot["city_state"],
            events=snapshot["events"]
        )
        
        self.db.add(db_state)
        self.db.commit()
    
    def _save_agent_actions(self, tick: int):
        """Save agent actions to database"""
        if not self.model:
            return
        
        # Get actions from agents' memory
        for agent_id, agent in self.model.agents.items():
            if agent.memory:
                latest_memory = agent.memory[-1]
                action = latest_memory.get("action", {})
                
                # Find or create agent in DB
                db_agent = self.db.query(Agent).filter(Agent.id == int(agent_id.split("_")[-1])).first()
                if not db_agent:
                    # Create agent if doesn't exist
                    from app.models.agent import AgentType
                    agent_type_map = {
                        "resident": AgentType.RESIDENT,
                        "transit_operator": AgentType.TRANSIT_OPERATOR,
                        "planner": AgentType.PLANNER,
                        "orchestrator": AgentType.ORCHESTRATOR
                    }
                    db_agent = Agent(
                        id=int(agent_id.split("_")[-1]) if agent_id.split("_")[-1].isdigit() else None,
                        agent_type=agent_type_map.get(agent.agent_type, AgentType.RESIDENT),
                        name=agent_id,
                        persona_config=agent.persona_config,
                        state=agent.state
                    )
                    self.db.add(db_agent)
                    self.db.flush()
                
                # Save action
                db_action = AgentAction(
                    agent_id=db_agent.id,
                    simulation_tick=tick,
                    action_type=action.get("action_type", "unknown"),
                    action_data=action.get("action_data", {}),
                    rationale=action.get("rationale", ""),
                    retrieved_docs=latest_memory.get("reasoning", {}).get("retrieved_docs"),
                    prompt_used=latest_memory.get("reasoning", {}).get("prompt_used"),
                    confidence_score=action.get("confidence", 0.5)
                )
                self.db.add(db_action)
        
        self.db.commit()
    
    def _save_final_metrics(self):
        """Calculate and save final simulation metrics"""
        if not self.model:
            return
        
        metrics = self.model.city_state.get("metrics", {})
        
        db_metrics = SimulationMetrics(
            run_id=self.run_id,
            avg_commute_time=metrics.get("avg_commute_time"),
            commute_time_change_pct=metrics.get("commute_time_change_pct"),
            transit_modal_share=metrics.get("transit_modal_share"),
            transit_ridership=sum(metrics.get("transit_ridership", {}).values()) if isinstance(metrics.get("transit_ridership"), dict) else metrics.get("transit_ridership", 0),
            emissions_proxy=metrics.get("emissions_proxy"),
            service_coverage=metrics.get("service_coverage"),
            job_access_30min=metrics.get("job_access_30min"),
            equity_index=metrics.get("equity_index"),
            metrics_json=metrics
        )
        
        self.db.add(db_metrics)
        self.db.commit()
    
    def cleanup(self):
        """Cleanup resources"""
        if self.db:
            self.db.close()
