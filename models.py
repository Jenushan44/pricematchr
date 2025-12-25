from sqlmodel import SQLModel
from sqlmodel import Field
from sqlmodel import Relationship
from typing import List
from typing import Optional 
from datetime import datetime

class Product(SQLModel, table=True):
  id: Optional[int] = Field(default = None, primary_key = True)
  name: str = Field(index = True) 

class PriceRecord(SQLModel, table = True): 
  id: Optional[int]  = Field(default = None, primary_key = True)
  price: float
  store_name: str 
  timestamp: datetime = Field(default_factory = datetime.utcnow)
  product_id: int = Field(foreign_key = "product.id") 