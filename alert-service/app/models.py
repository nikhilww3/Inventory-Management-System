from sqlalchemy import Column, Integer, Boolean
from app.database import Base
# type of contain in table of alert
class Alert(Base):
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    threshold = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    
