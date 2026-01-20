"""
Celery tasks for data ingestion
"""
from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.data import CityData
import structlog
import osmnx as ox
import networkx as nx
import json

logger = structlog.get_logger()


@celery_app.task(bind=True, name="process_city_data")
def process_city_data_task(self, city_data_id: int):
    """Process city data (e.g., from OSM)"""
    logger.info("Starting city data processing", city_data_id=city_data_id, task_id=self.request.id)
    
    db = SessionLocal()
    try:
        city_data = db.query(CityData).filter(CityData.id == city_data_id).first()
        if not city_data:
            logger.error("City data not found", city_data_id=city_data_id)
            return {"status": "error", "message": "City data not found"}
        
        city_data.status = "processing"
        db.commit()
        
        # Process based on data type
        if city_data.data_type == "osm":
            processed_data = _process_osm_data(city_data)
        else:
            processed_data = {}
        
        # Update city data
        city_data.geometry = processed_data
        city_data.status = "completed"
        city_data.processed_at = db.func.now()
        db.commit()
        
        logger.info("City data processing completed", city_data_id=city_data_id)
        return {"status": "completed", "city_data_id": city_data_id}
        
    except Exception as e:
        logger.error("City data processing failed", error=str(e), city_data_id=city_data_id)
        city_data = db.query(CityData).filter(CityData.id == city_data_id).first()
        if city_data:
            city_data.status = "failed"
            db.commit()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


def _process_osm_data(city_data: CityData) -> dict:
    """Process OpenStreetMap data"""
    # Get city name or use default
    city_name = city_data.city_name or "San Francisco, California, USA"
    
    try:
        # Download street network
        G = ox.graph_from_place(city_name, network_type="drive")
        
        # Convert to nodes and edges
        nodes = []
        for node_id, data in G.nodes(data=True):
            nodes.append({
                "id": str(node_id),
                "attributes": {
                    "x": data.get("x", 0),
                    "y": data.get("y", 0),
                    "lat": data.get("y", 0),
                    "lon": data.get("x", 0)
                }
            })
        
        edges = []
        for u, v, data in G.edges(data=True):
            edges.append({
                "source": str(u),
                "target": str(v),
                "weight": data.get("length", 1.0),
                "attributes": {
                    "length": data.get("length", 1.0),
                    "highway": data.get("highway", "unknown")
                }
            })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "city_name": city_name,
                "node_count": len(nodes),
                "edge_count": len(edges)
            }
        }
    except Exception as e:
        logger.error("OSM processing failed", error=str(e))
        # Return empty structure
        return {
            "nodes": [],
            "edges": [],
            "metadata": {"error": str(e)}
        }
