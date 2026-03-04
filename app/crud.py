from sqlalchemy.orm import Session, session
from app import models, schemas

def create_item(db:session, item: schemas.InventoryCreate):
    db_item = models.InventoryItem(name=item.name, category=item.category, quantity=item.quantity, threshold=item.threshold)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db:session):
    return db.query(models.InventoryItem).all()

def get_item(db:session, item_id: int):
    return db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).first()

def update_item(db:session, item_id: int, quantity: int):
    item = get_item(db, item_id)
    if item:
        item.quantity = quantity
        db.commit()
        db.refresh(item)
    return item

def delete_item(db:session, item_id: int):
    item = get_item(db, item_id)
    if item:
        db.delete(item)
        db.commit()
    return item