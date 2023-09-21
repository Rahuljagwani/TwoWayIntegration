from sqlalchemy import inspect
from psql import SessionLocal, engine
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

def create_record_in_db(db_model, data, model):
    db = SessionLocal()
    try:
        insp = inspect(engine)
        if not insp.has_table(db_model.__tablename__):
            db_model.metadata.create_all(bind=engine)

        instance = db_model(**{field: data[field] for field in model.__annotations__.keys()})
        print(instance)
        new_record = db_model(**{field: data[field] for field in model.__annotations__.keys()})
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        db.close()
        return new_record
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Database integrity violation(Either id repeated or val not string)") from e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error") from e

    
        
    
