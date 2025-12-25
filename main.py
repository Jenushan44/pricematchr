from fastapi import FastAPI
from sqlmodel import SQLModel
from sqlmodel import create_engine
from models import Product
from models import PriceRecord

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