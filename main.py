from fastapi import FastAPI
from sqlmodel import SQLModel
from database import engine, create_db_and_tables, get_session 
from models import Product, PriceRecord

# creates the main web server object that manages the routes and handles any incoming requests
app = FastAPI()

@app.on_event("startup")
def on_startup():
  create_db_and_tables()