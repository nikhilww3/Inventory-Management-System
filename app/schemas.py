from pydantic import BaseModel, ConfigDict

class InventoryCreate(BaseModel):
    name: str
    category: str
    quantity: int
    threshold: int
    
class InventoryUpdate(BaseModel):
    quantity: int

class InventoryResponse(BaseModel):
    id: int
    name: str
    category: str
    quantity: int
    threshold: int
    
    model_config = ConfigDict(from_attributes=True)