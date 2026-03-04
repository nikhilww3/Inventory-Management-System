
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import database, models, schemas, logic

# create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Alert Service")

# create a fresh session of database for SessionLocal
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# api call to check alert system
@app.post("/check-alert")
def check_alert(data: schemas.AlertCheck, db: Session = Depends(get_db)):
    result = logic.check_and_create_alert(
        db,
        data.item_id,
        data.quantity,
        data.threshold
    )
    return result

# get all alert system 
@app.get("/alerts", response_model=list[schemas.AlertResponse])
def get_alerts(db: Session = Depends(get_db)):
    return db.query(models.Alert).all()
