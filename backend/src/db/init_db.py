#!/usr/bin/env python3
"""
Initialize the database with tables.

This script:
1. Creates database connection
2. Creates all required tables
3. Populates with initial data if needed
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.config import settings
from backend.src.db.models import Base, ChatbotQuery, UserPreference


def init_database():
    """Initialize the database."""
    # Create engine
    database_url = settings.database_url

    if not database_url:
        print("Warning: DATABASE_URL not configured. Skipping database initialization.")
        print("Set DATABASE_URL environment variable to enable persistent storage.")
        return

    print(f"Connecting to database: {database_url.split('@')[1] if '@' in database_url else '...'}")

    engine = create_engine(database_url, echo=False)

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")

    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    # Check if tables exist and have data
    try:
        query_count = session.query(ChatbotQuery).count()
        preference_count = session.query(UserPreference).count()

        print(f"Current data:")
        print(f"  ChatbotQuery records: {query_count}")
        print(f"  UserPreference records: {preference_count}")

    except Exception as e:
        print(f"Error checking database: {e}")
    finally:
        session.close()

    print("Database initialization complete")


if __name__ == "__main__":
    init_database()
