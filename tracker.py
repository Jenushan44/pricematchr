from sqlmodel import Session, select 
from database import engine 
from models import Product, PriceRecord 
from scraper import get_price 
import datetime 

def update_prices(): 
  with Session(engine) as session: 
    statement = select(Product)
    products = session.exec(statement).all()
    print("Starting updates at ", datetime.datetime.now())
    
    for product in products: 
      print("Checking: ", product.name)
      current_price = get_price(product.url)

      if current_price: 
        new_record = PriceRecord(
          price = current_price, 
          store_name = "Amazon", 
          product_id = product.id
        )
        session.add(new_record)

        if current_price <= product.target_price: 
          print("Alert: ", product.name, "is now $", current_price)
        else: 
          print("No deal yet. Current price: $", current_price)
    
    session.commit()
    print("Update finished")

if __name__ == "__main__":
  update_prices()