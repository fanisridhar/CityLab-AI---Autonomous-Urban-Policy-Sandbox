"""
Tests for database models
"""
import pytest
from app.models.scenario import Scenario
from app.models.agent import Agent, AgentType


def test_scenario_model(db_session):
    """Test Scenario model creation"""
    scenario = Scenario(
        name="Test Scenario",
        description="Test description",
        policy_type="congestion_pricing",
        policy_config={"price": 5.0}
    )
    db_session.add(scenario)
    db_session.commit()
    db_session.refresh(scenario)
    
    assert scenario.id is not None
    assert scenario.name == "Test Scenario"
    assert scenario.policy_type == "congestion_pricing"
    db_session.delete(scenario)
    db_session.commit()


def test_agent_model(db_session):
    """Test Agent model creation"""
    agent = Agent(
        agent_type=AgentType.RESIDENT,
        name="Test Resident",
        persona_config={"home_location": [0, 0]},
        state={"current_location": [0, 0]}
    )
    db_session.add(agent)
    db_session.commit()
    db_session.refresh(agent)
    
    assert agent.id is not None
    assert agent.agent_type == AgentType.RESIDENT
    assert agent.name == "Test Resident"
    db_session.delete(agent)
    db_session.commit()
