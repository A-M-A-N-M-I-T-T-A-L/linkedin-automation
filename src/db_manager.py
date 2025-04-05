import chromadb
from chromadb.config import Settings
from config.config import DB_PATH
import logging

logger = logging.getLogger(__name__)

class DBManager:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=DB_PATH
        ))
        self.jobs_collection = self.client.get_or_create_collection("jobs")
        self.profiles_collection = self.client.get_or_create_collection("profiles")
        
    def store_job(self, job_data, embedding):
        try:
            self.jobs_collection.add(
                documents=[job_data],
                embeddings=[embedding],
                ids=[job_data['job_id']]
            )
            logger.info(f"Stored job {job_data['job_id']}")
        except Exception as e:
            logger.error(f"Error storing job: {str(e)}")
    
    def query_similar_jobs(self, query_embedding, n_results=5):
        return self.jobs_collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        ) 