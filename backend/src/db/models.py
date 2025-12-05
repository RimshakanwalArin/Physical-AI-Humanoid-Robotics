from sqlalchemy import Column, String, Float, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ChatbotQuery(Base):
    """Model for storing chatbot queries"""
    __tablename__ = "chatbot_queries"
    
    id = Column(String, primary_key=True)
    query_text = Column(String)
    session_id = Column(String)
    embedding_vector = Column(JSON)
    retrieved_sections = Column(JSON)
    response_text = Column(String)
    source_citations = Column(JSON)
    latency_ms = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    accuracy_label = Column(String, nullable=True)

class UserPreference(Base):
    """Model for user preferences (optional)"""
    __tablename__ = "user_preferences"
    
    session_id = Column(String, primary_key=True)
    personalization_level = Column(String, default="BEGINNER")
    language = Column(String, default="EN")
    last_chapter_viewed = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
