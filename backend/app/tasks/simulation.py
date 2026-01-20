"""
Celery tasks for simulation execution
"""
from app.core.celery_app import celery_app
from app.simulation.simulation_engine import SimulationEngine
from app.core.database import SessionLocal
from app.models.scenario import Scenario, ScenarioRun
from app.models.data import CityData
import structlog

logger = structlog.get_logger()


@celery_app.task(bind=True, name="run_simulation")
def run_simulation_task(self, run_id: int):
    """Run a simulation asynchronously"""
    logger.info("Starting simulation task", run_id=run_id, task_id=self.request.id)
    
    db = SessionLocal()
    try:
        # Get scenario run
        run = db.query(ScenarioRun).filter(ScenarioRun.id == run_id).first()
        if not run:
            logger.error("Scenario run not found", run_id=run_id)
            return {"status": "error", "message": "Scenario run not found"}
        
        # Get scenario
        scenario = db.query(Scenario).filter(Scenario.id == run.scenario_id).first()
        if not scenario:
            logger.error("Scenario not found", scenario_id=run.scenario_id)
            return {"status": "error", "message": "Scenario not found"}
        
        # Get city data
        city_data_obj = None
        if scenario.city_data_id:
            city_data_obj = db.query(CityData).filter(CityData.id == scenario.city_data_id).first()
        
        # Prepare configuration
        city_data = city_data_obj.geometry if city_data_obj and city_data_obj.geometry else {}
        scenario_config = {
            "name": scenario.name,
            "policy_type": scenario.policy_type,
            "policy_config": scenario.policy_config or {}
        }
        
        # TODO: Get agents config from scenario or defaults
        agents_config = [
            {
                "agent_type": "orchestrator",
                "persona_config": {
                    "scenario_config": scenario_config,
                    "simulation_days": run.simulation_days
                }
            }
        ]
        
        # Initialize and run simulation
        engine = SimulationEngine(run_id)
        engine.initialize(
            scenario_config=scenario_config,
            city_data=city_data,
            agents_config=agents_config,
            seed=run.seed
        )
        
        engine.run(simulation_days=run.simulation_days)
        engine.cleanup()
        
        logger.info("Simulation task completed", run_id=run_id)
        return {"status": "completed", "run_id": run_id}
        
    except Exception as e:
        logger.error("Simulation task failed", error=str(e), run_id=run_id)
        run = db.query(ScenarioRun).filter(ScenarioRun.id == run_id).first()
        if run:
            run.status = "failed"
            run.error_message = str(e)
            db.commit()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
