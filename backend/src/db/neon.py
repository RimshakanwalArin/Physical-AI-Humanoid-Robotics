import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

logger = logging.getLogger(__name__)

class NeonConnection:
    """Connection manager for Neon PostgreSQL"""
    
    _engine = None
    _SessionLocal = None
    
    @classmethod
    def init_db(cls, database_url: str):
        """Initialize database connection"""
        if database_url:
            try:
                cls._engine = create_engine(database_url, echo=False)
                cls._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls._engine)
                Base.metadata.create_all(bind=cls._engine)
                logger.info("Database initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize database: {e}")
        else:
            logger.warning("NEON_DATABASE_URL not provided, skipping database initialization")
    
    @classmethod
    def get_session(cls):
        """Get database session"""
        if cls._SessionLocal:
            return cls._SessionLocal()
        return None
    
    @classmethod
    def save_query(cls, chatbot_query):
        """Save chatbot query to database"""
        session = cls.get_session()
        if session:
            try:
                session.add(chatbot_query)
                session.commit()
                logger.info(f"Query saved: {chatbot_query.id}")
            except Exception as e:
                logger.error(f"Error saving query: {e}")
                session.rollback()
            finally:
                session.close()
