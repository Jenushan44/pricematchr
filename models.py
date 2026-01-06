from sqlmodel import SQLModel
from sqlmodel import Field
from sqlmodel import Relationship
from typing import List
from typing import Optional 
from datetime import datetime

class Product(SQLModel, table=True):
  # id set to Optional so that it may be an integer or set to None for a little while
  # Field() is used to store the metadata
  id: Optional[int] = Field(default = None, primary_key = True)
  name: str = Field(index = True) 
  url: str 
  target_price: float 
  user_email: str
  price_records: List["PriceRecord"] = Relationship(back_populates= "product")

class PriceRecord(SQLModel, table = True): 
  id: Optional[int]  = Field(default = None, primary_key = True)
  price: float
  store_name: str 
  timestamp: datetime = Field(default_factory = datetime.utcnow)
  product_id: int = Field(foreign_key = "product.id")
  product: Product = Relationship(back_populates="price_records") 