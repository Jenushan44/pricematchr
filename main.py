from fastapi import FastAPI
from sqlmodel import SQLModel
from sqlmodel import create_engine
from models import Product
from models import PriceRecord
from sqlmodel import Session
from fastapi import Depends 
from sqlmodel import select

def get_session():
  with Session(engine) as session: 
    yield session

# url that acts as a connection string that tells the application where the database is located and how to get in
sqlite_url = "postgresql://myuser:mypassword@localhost:5433/pricematchr_db"
engine = create_engine(sqlite_url) # connector that is active while the app is running transfering data between the application and database

# creates the main web server object that manages the routes and handles any incoming requests
app = FastAPI()

@app.on_event("startup")
def on_startup():
  SQLModel.metadata.create_all(engine) # looks at python classes and creates any missing tables in the database

@app.get("/")
def root(): 
  return {"message": "PriceMatchr API is running and the database is connected"}

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