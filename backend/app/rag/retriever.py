"""
Document retriever for RAG
"""
from typing import List, Dict, Any, Optional
from app.rag.vector_store import vector_store
from app.core.database import SessionLocal
from app.models.data import PolicyDocument
import structlog

logger = structlog.get_logger()


class DocumentRetriever:
    """Retrieve relevant policy documents for agents"""
    
    def __init__(self):
        self.vector_store = vector_store
        self.db = SessionLocal()
    
    def retrieve_for_agent(
        self,
        agent_type: str,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for an agent"""
        # Enhance query with agent context
        enhanced_query = self._enhance_query(agent_type, query, context)
        
        # Filter metadata based on agent type
        filter_metadata = self._get_filter_metadata(agent_type, context)
        
        # Search vector store
        results = self.vector_store.search(
            query=enhanced_query,
            n_results=n_results,
            filter_metadata=filter_metadata
        )
        
        # Enrich with full document data
        enriched_results = []
        for result in results:
            doc_id = result["id"]
            db_doc = self.db.query(PolicyDocument).filter(
                PolicyDocument.vector_id == doc_id
            ).first()
            
            if db_doc:
                enriched_results.append({
                    "id": doc_id,
                    "title": db_doc.title,
                    "document_type": db_doc.document_type,
                    "source": db_doc.source,
                    "content": result["content"],
                    "metadata": result["metadata"],
                    "effective_date": db_doc.effective_date.isoformat() if db_doc.effective_date else None,
                    "relevance_score": 1.0 - result.get("distance", 1.0)  # Convert distance to similarity
                })
        
        return enriched_results
    
    def _enhance_query(self, agent_type: str, query: str, context: Optional[Dict]) -> str:
        """Enhance query with agent-specific context"""
        enhancements = {
            "planner": "urban planning policy regulation budget",
            "transit_operator": "transit public transportation route frequency budget",
            "resident": "transportation policy fare pricing accessibility",
            "developer": "zoning development regulation building",
            "business": "commercial zoning business regulation"
        }
        
        enhancement = enhancements.get(agent_type, "")
        return f"{query} {enhancement}"
    
    def _get_filter_metadata(self, agent_type: str, context: Optional[Dict]) -> Optional[Dict]:
        """Get filter metadata for vector search"""
        # Can filter by document_type, effective_date, etc.
        return None  # No filtering for now
    
    def close(self):
        """Close database connection"""
        if self.db:
            self.db.close()
