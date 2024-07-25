from sqlalchemy.orm import Session
from app.database import SessionLocal, engine

def test_db_connection():
    try:
        db: Session = SessionLocal()
        result = db.execute("SELECT 1")
        print("Connection successful:", result.fetchone())
    except Exception as e:
        print("Connection failed:", str(e))
    finally:
        db.close()

if __name__ == "__main__":
    test_db_connection()
