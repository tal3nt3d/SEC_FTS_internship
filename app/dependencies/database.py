from app.database.database import SessionLocal

def get_db():
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        print(e)
        db.rollback()
        raise
    finally:
        db.close()