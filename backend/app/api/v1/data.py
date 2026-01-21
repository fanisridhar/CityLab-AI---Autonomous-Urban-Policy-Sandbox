"""
Data ingestion API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.models.data import CityData, PolicyDocument

router = APIRouter()


class CityDataResponse(BaseModel):
    id: int
    name: str
    city_name: Optional[str]
    region: Optional[str]
    data_type: str
    source_url: Optional[str]
    status: str
    metadata_json: Optional[dict]  # Maps to metadata_json attribute
    created_at: datetime
    
    class Config:
        from_attributes = True


class PolicyDocumentResponse(BaseModel):
    id: int
    title: str
    document_type: Optional[str]
    source: Optional[str]
    metadata_json: Optional[dict]
    effective_date: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.post("/city", response_model=CityDataResponse, status_code=201)
async def create_city_data(
    name: str,
    city_name: Optional[str] = None,
    data_type: str = "osm",
    source_url: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Create a new city data entry"""
    city_data = CityData(
        name=name,
        city_name=city_name,
        data_type=data_type,
        source_url=source_url,
        status="pending"
    )
    db.add(city_data)
    db.commit()
    db.refresh(city_data)
    
    # TODO: Trigger background processing task
    # from app.tasks.data_ingestion import process_city_data_task
    # process_city_data_task.delay(city_data.id)
    
    return city_data


@router.get("/city", response_model=List[CityDataResponse])
async def list_city_data(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all city data entries"""
    data = db.query(CityData).offset(skip).limit(limit).all()
    return data


@router.get("/city/{data_id}", response_model=CityDataResponse)
async def get_city_data(
    data_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific city data entry"""
    data = db.query(CityData).filter(CityData.id == data_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="City data not found")
    return data


@router.post("/policy", response_model=PolicyDocumentResponse, status_code=201)
async def create_policy_document(
    title: str,
    document_type: Optional[str] = None,
    source: Optional[str] = None,
    content: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Create a new policy document"""
    doc = PolicyDocument(
        title=title,
        document_type=document_type,
        source=source,
        content=content
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    # TODO: Trigger embedding generation task
    # from app.tasks.rag import index_policy_document_task
    # index_policy_document_task.delay(doc.id)
    
    return doc


@router.get("/policy", response_model=List[PolicyDocumentResponse])
async def list_policy_documents(
    document_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List policy documents"""
    query = db.query(PolicyDocument)
    if document_type:
        query = query.filter(PolicyDocument.document_type == document_type)
    docs = query.offset(skip).limit(limit).all()
    return docs
