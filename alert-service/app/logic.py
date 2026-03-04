from sqlalchemy.orm import Session
from app import models

def check_and_create_alert(db: Session, item_id: int, quantity: int, threshold:int):
    existing_alert = db.query(models.Alert).filter(
        models.Alert.item_id == item_id,
        models.Alert.is_active == True
    ).first()
    
    # case 1: Stock below threshlod value
    if quantity < threshold:
        if not existing_alert:
           alert = models.Alert(
           item_id = item_id,
           quantity = quantity,
           threshold = threshold,
           is_active = True
           )
        
           db.add(alert)
           db.commit()
           db.refresh(alert)
           return {"message": "Alert Created", "Alert Id" : alert.id}
        return  {"message" : "alert alread active"}
    
    # case 2 when stock refill 
    
    if quantity >= threshold and existing_alert:
        existing_alert.is_active = False
        db.commit()
        
        return {"meassage" : "Alert resolved"}
    return {"message" : "stock level recovered"}
        
      
