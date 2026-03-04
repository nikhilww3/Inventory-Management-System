from pydantic import BaseModel, ConfigDict

class AlertCheck(BaseModel):
    item_id: int
    quantity: int
    threshold: int
    
    
class AlertResponse(BaseModel):
    id: int
    item_id: int
    quantity: int
    threshold: int
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)