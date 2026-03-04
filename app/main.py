from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud, database
import requests

# create the database
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Inventory service")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# api crud calls
    
@app.get("/")
def read_root():
    return {"message": "Inventory service is running"}

@app.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    items = crud.get_items(db)

    total_items = len(items)
    raw_count = sum(1 for item in items if item.category.lower() == "raw")
    finished_count = sum(1 for item in items if item.category.lower() == "finished")
    total_quantity = sum(item.quantity for item in items)
    low_stock_count = sum(1 for item in items if item.quantity < item.threshold)

    return {
        "total_items": total_items,
        "raw_materials": raw_count,
        "finished_goods": finished_count,
        "total_quantity": total_quantity,
        "low_stock_items": low_stock_count
    }

@app.post("/items/", response_model=schemas.InventoryResponse)
def create_item(item: schemas.InventoryCreate, db: Session = Depends(get_db)):
    db_item = crud.create_item(db, item)
    return db_item

@app.get("/items/", response_model=list[schemas.InventoryResponse])
def get_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

import requests

@app.put("/items/{item_id}")
def update_item(item_id: int, update: schemas.InventoryUpdate, db: Session = Depends(get_db)):
    item = crud.update_item(db, item_id, update.quantity)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    try:
        response = requests.post(
            "http://127.0.0.1:8001/check-alert",
            json={
                "item_id": item.id,
                "quantity": item.quantity,
                "threshold": item.threshold
            }
        )
        print("Alert Service Response:", response.json())
    except Exception as e:
        print("Error contacting Alert Service:", e)

    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.delete_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
    


