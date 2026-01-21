"""
Data ingestion models
"""
from sqlalchemy import Column, Integer, String, JSON, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class CityData(Base):
    """Imported city data (GIS, transit networks, etc.)"""
    __tablename__ = "city_data"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    city_name = Column(String(255))
    region = Column(String(255))
    
    # Data sources
    data_type = Column(String(100))  # e.g., "osm", "gis", "transit_gtfs"
    source_url = Column(String(500))
    file_path = Column(String(500))
    
    # Data content
    metadata_json = Column(JSON, name="metadata")  # Data-specific metadata (column name is metadata in DB)
    geometry = Column(JSON)  # GeoJSON or similar
    
    # Processing status
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    processed_at = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    scenarios = relationship("Scenario", back_populates="city_data")


class PolicyDocument(Base):
    """Policy documents for RAG"""
    __tablename__ = "policy_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    document_type = Column(String(100))  # e.g., "regulation", "budget", "case_study"
    source = Column(String(500))
    content = Column(Text)
    
    # Vector DB reference
    vector_id = Column(String(255))  # ID in vector database
    
    # Metadata
    metadata_json = Column(JSON)
    effective_date = Column(DateTime(timezone=True))
    expiration_date = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
