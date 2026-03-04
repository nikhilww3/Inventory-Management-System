from unicodedata import category
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class InventoryItem(Base):
    __tablename__ = "inventory_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # category = raw/finished
    category = Column(String, nullable=False) 
    quantity = Column(Integer, nullable=False)
    threshold = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    
    
    
    