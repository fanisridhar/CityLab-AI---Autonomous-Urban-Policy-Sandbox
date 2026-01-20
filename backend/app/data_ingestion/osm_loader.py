"""
OpenStreetMap data loader
"""
from typing import Dict, Any
import osmnx as ox
import networkx as nx
import structlog

logger = structlog.get_logger()


def load_city_from_osm(city_name: str, network_type: str = "drive") -> Dict[str, Any]:
    """Load city street network from OpenStreetMap"""
    try:
        logger.info("Loading OSM data", city_name=city_name, network_type=network_type)
        
        # Download street network
        G = ox.graph_from_place(city_name, network_type=network_type)
        
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
                    "highway": data.get("highway", "unknown"),
                    "name": data.get("name", "")
                }
            })
        
        # Get bounding box
        bbox = ox.utils_geo.bbox_from_point(
            (G.nodes[list(G.nodes())[0]]["y"], G.nodes[list(G.nodes())[0]]["x"]),
            dist=5000
        )
        
        result = {
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "city_name": city_name,
                "network_type": network_type,
                "node_count": len(nodes),
                "edge_count": len(edges),
                "bbox": bbox
            }
        }
        
        logger.info("OSM data loaded", nodes=len(nodes), edges=len(edges))
        return result
        
    except Exception as e:
        logger.error("Failed to load OSM data", error=str(e), city_name=city_name)
        raise
