from sqlalchemy import inspect
from TwoWayIntegration.database.psql import SessionLocal, engine
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException

def create_record_in_db(db_model, data, model):
    db = SessionLocal()
    try:
        insp = inspect(engine)
        if not insp.has_table(db_model.__tablename__):
            db_model.metadata.create_all(bind=engine)
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

def update_record_in_db(db_model, record_id, model, data):
    db = SessionLocal()
    insp = inspect(engine)
    if not insp.has_table(db_model.__tablename__):
        db_model.metadata.create_all(bind=engine)

    try:
        if isinstance(data, dict):
            db_record = db.query(db_model).filter(db_model.id == record_id).first()
            if db_record:
                for key, value in data.items():
                    setattr(db_record, key, value)
                db.commit()
                db.refresh(db_record)
                db.close()
                return db_record
            else:
                raise HTTPException(status_code=404, detail="Record not found")
        else:
            raise ValueError("Data must be a dictionary")

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Database error") from e
    except ValueError as ve:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error") from e

def delete_record_in_db(db_model, record_id):
    db = SessionLocal()
    try:
        existing_record = db.query(db_model).filter(db_model.id == record_id).first()
        if existing_record:
            db.delete(existing_record)
            db.commit()
            db.close()
            return {"message": f"{db_model.__name__} with id {record_id} deleted"}
        else:
            db.close()
            raise HTTPException(status_code=404, detail=f"{db_model.__name__} not found")

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error") from e

