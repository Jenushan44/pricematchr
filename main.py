from fastapi import FastAPI, Depends 
from sqlmodel import Session, select  
from database import get_session, engine, create_db_and_tables
from models import Product, PriceRecord

app = FastAPI()

@app.on_event("startup")
def on_startup():
  create_db_and_tables()

@app.post("/products")
def create_product(product: Product, session: Session = Depends(get_session)):
  session.add(product)
  session.commit()

  session.refresh(product)
  return product


@app.get("/products")
def read_products(session: Session = Depends(get_session)):
  products = session.exec(select(Product)).all()
  return products