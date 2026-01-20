"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # City data table
    op.create_table(
        'city_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('city_name', sa.String(length=255), nullable=True),
        sa.Column('region', sa.String(length=255), nullable=True),
        sa.Column('data_type', sa.String(length=100), nullable=True),
        sa.Column('source_url', sa.String(length=500), nullable=True),
        sa.Column('file_path', sa.String(length=500), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('geometry', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('processed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_city_data_id'), 'city_data', ['id'], unique=False)
    
    # Policy documents table
    op.create_table(
        'policy_documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('document_type', sa.String(length=100), nullable=True),
        sa.Column('source', sa.String(length=500), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('vector_id', sa.String(length=255), nullable=True),
        sa.Column('metadata_json', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('effective_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expiration_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Scenarios table
    op.create_table(
        'scenarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('policy_type', sa.String(length=100), nullable=True),
        sa.Column('policy_config', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('city_data_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(['city_data_id'], ['city_data.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scenarios_id'), 'scenarios', ['id'], unique=False)
    op.create_index(op.f('ix_scenarios_name'), 'scenarios', ['name'], unique=False)
    
    # Scenario runs table
    op.create_table(
        'scenario_runs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('scenario_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('simulation_days', sa.Integer(), nullable=True),
        sa.Column('start_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('seed', sa.Integer(), nullable=True),
        sa.Column('metrics', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['scenario_id'], ['scenarios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scenario_runs_id'), 'scenario_runs', ['id'], unique=False)
    
    # Agents table
    op.create_table(
        'agents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('agent_type', sa.Enum('RESIDENT', 'TRANSIT_OPERATOR', 'PLANNER', 'DEVELOPER', 'BUSINESS', 'EMERGENCY_SERVICE', 'ORCHESTRATOR', name='agenttype'), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('persona_config', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('location', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('state', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('memory_store_id', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_agents_id'), 'agents', ['id'], unique=False)
    op.create_index(op.f('ix_agents_agent_type'), 'agents', ['agent_type'], unique=False)
    
    # Agent actions table
    op.create_table(
        'agent_actions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('agent_id', sa.Integer(), nullable=False),
        sa.Column('simulation_tick', sa.Integer(), nullable=False),
        sa.Column('action_type', sa.String(length=100), nullable=True),
        sa.Column('action_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('rationale', sa.Text(), nullable=True),
        sa.Column('retrieved_docs', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('prompt_used', sa.Text(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Simulation states table
    op.create_table(
        'simulation_states',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('run_id', sa.Integer(), nullable=False),
        sa.Column('tick', sa.Integer(), nullable=False),
        sa.Column('simulation_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('agent_states', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('city_state', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('events', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['run_id'], ['scenario_runs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_simulation_states_id'), 'simulation_states', ['id'], unique=False)
    op.create_index(op.f('ix_simulation_states_tick'), 'simulation_states', ['tick'], unique=False)
    
    # Simulation metrics table
    op.create_table(
        'simulation_metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('run_id', sa.Integer(), nullable=False),
        sa.Column('avg_commute_time', sa.Float(), nullable=True),
        sa.Column('commute_time_change_pct', sa.Float(), nullable=True),
        sa.Column('transit_modal_share', sa.Float(), nullable=True),
        sa.Column('transit_ridership', sa.Integer(), nullable=True),
        sa.Column('emissions_proxy', sa.Float(), nullable=True),
        sa.Column('service_coverage', sa.Float(), nullable=True),
        sa.Column('job_access_30min', sa.Float(), nullable=True),
        sa.Column('equity_index', sa.Float(), nullable=True),
        sa.Column('metrics_json', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['run_id'], ['scenario_runs.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('run_id')
    )


def downgrade() -> None:
    op.drop_table('simulation_metrics')
    op.drop_table('simulation_states')
    op.drop_table('agent_actions')
    op.drop_table('agents')
    op.drop_table('scenario_runs')
    op.drop_table('scenarios')
    op.drop_table('policy_documents')
    op.drop_table('city_data')
