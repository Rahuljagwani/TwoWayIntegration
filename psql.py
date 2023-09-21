# database/psql.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_CONNECTION_PARAMS

# Create a SQLAlchemy engine and session
engine = create_engine(
    f"postgresql://{DB_CONNECTION_PARAMS['user']}:{DB_CONNECTION_PARAMS['password']}@{DB_CONNECTION_PARAMS['host']}:{DB_CONNECTION_PARAMS['port']}/{DB_CONNECTION_PARAMS['database']}"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
