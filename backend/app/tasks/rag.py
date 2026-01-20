"""
Celery tasks for RAG operations
"""
from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.data import PolicyDocument
from app.rag.vector_store import vector_store
from langchain.text_splitter import RecursiveCharacterTextSplitter
import structlog

logger = structlog.get_logger()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)


@celery_app.task(bind=True, name="index_policy_document")
def index_policy_document_task(self, document_id: int):
    """Index a policy document in the vector store"""
    logger.info("Starting document indexing", document_id=document_id, task_id=self.request.id)
    
    db = SessionLocal()
    try:
        doc = db.query(PolicyDocument).filter(PolicyDocument.id == document_id).first()
        if not doc:
            logger.error("Policy document not found", document_id=document_id)
            return {"status": "error", "message": "Policy document not found"}
        
        if not doc.content:
            logger.warning("Document has no content", document_id=document_id)
            return {"status": "skipped", "message": "No content to index"}
        
        # Split document into chunks
        chunks = text_splitter.split_text(doc.content)
        
        # Index each chunk
        for i, chunk in enumerate(chunks):
            chunk_id = f"{document_id}_chunk_{i}"
            metadata = {
                "document_id": document_id,
                "title": doc.title,
                "document_type": doc.document_type or "unknown",
                "source": doc.source or "",
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            
            vector_store.add_document(
                document_id=chunk_id,
                content=chunk,
                metadata=metadata
            )
        
        # Update document with vector ID reference
        doc.vector_id = f"{document_id}_chunk_0"  # Reference to first chunk
        db.commit()
        
        logger.info("Document indexing completed", document_id=document_id, chunks=len(chunks))
        return {"status": "completed", "document_id": document_id, "chunks": len(chunks)}
        
    except Exception as e:
        logger.error("Document indexing failed", error=str(e), document_id=document_id)
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
