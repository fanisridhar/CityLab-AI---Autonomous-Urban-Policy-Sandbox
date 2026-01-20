"""
Vector store for policy documents using Chroma or Pinecone
"""
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
import structlog
from app.core.config import settings

logger = structlog.get_logger()


class VectorStore:
    """Vector store for policy documents"""
    
    def __init__(self):
        self.client = None
        self.collection = None
        self._initialize()
    
    def _initialize(self):
        """Initialize vector store"""
        if settings.USE_PINECONE:
            # TODO: Implement Pinecone
            logger.warning("Pinecone not yet implemented, using Chroma")
        
        # Use Chroma
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIRECTORY,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="policy_documents",
            metadata={"hnsw:space": "cosine"}
        )
        
        logger.info("Vector store initialized", collection="policy_documents")
    
    def add_document(
        self,
        document_id: str,
        content: str,
        metadata: Dict[str, Any]
    ):
        """Add a document to the vector store"""
        try:
            self.collection.add(
                ids=[document_id],
                documents=[content],
                metadatas=[metadata]
            )
            logger.info("Document added to vector store", document_id=document_id)
        except Exception as e:
            logger.error("Failed to add document", error=str(e), document_id=document_id)
            raise
    
    def update_document(
        self,
        document_id: str,
        content: str,
        metadata: Dict[str, Any]
    ):
        """Update a document in the vector store"""
        try:
            self.collection.update(
                ids=[document_id],
                documents=[content],
                metadatas=[metadata]
            )
            logger.info("Document updated in vector store", document_id=document_id)
        except Exception as e:
            logger.error("Failed to update document", error=str(e), document_id=document_id)
            raise
    
    def delete_document(self, document_id: str):
        """Delete a document from the vector store"""
        try:
            self.collection.delete(ids=[document_id])
            logger.info("Document deleted from vector store", document_id=document_id)
        except Exception as e:
            logger.error("Failed to delete document", error=str(e), document_id=document_id)
            raise
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        try:
            where = filter_metadata if filter_metadata else None
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where
            )
            
            # Format results
            documents = []
            if results["ids"] and len(results["ids"][0]) > 0:
                for i in range(len(results["ids"][0])):
                    documents.append({
                        "id": results["ids"][0][i],
                        "content": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "distance": results["distances"][0][i] if "distances" in results else None
                    })
            
            return documents
        except Exception as e:
            logger.error("Vector search failed", error=str(e))
            return []


# Singleton instance
vector_store = VectorStore()
