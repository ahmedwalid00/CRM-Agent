"""
This module provides functions to manage the database connection lifecycle
for standalone scripts and services.
"""
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def setup_database_engine(db_uri: str):
    """
    Creates and returns the SQLAlchemy engine and a Session factory.
    Exits the program if the connection fails.
    """
    if not db_uri:
        print("FATAL: Database URI is not configured.", file=sys.stderr)
        sys.exit(1)
        
    try:
        engine = create_engine(db_uri)
        # Test connection on startup
        with engine.connect() as connection:
            print("Database engine created and connection successful.")
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return engine, SessionLocal
    except Exception as e:
        print(f"FATAL: Failed to connect to database using the provided URI.", file=sys.stderr)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)