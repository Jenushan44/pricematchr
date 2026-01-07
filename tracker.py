from sqlmodel import Session, select 
from database import engine 
from models import Product, PriceRecord 
from scraper import get_price 
import datetime 
import time
from notifications import send_price_alert

def update_prices(): 
  with Session(engine) as session: 
    products = session.exec(select(Product)).all()
    print("Starting check ", datetime.datetime.now())
    
    
    for product in products: 
      try: 
        print("Checking: ", product.name)
        current_price = get_price(product.url)

        if current_price: 
          if len(product.price_records) > 0: 
            last_price = product.price_records[-1].price
          else: 
            last_price = None 
          
          new_record = PriceRecord(price = current_price, store_name= "Amazon", product_id = product.id) 
          session.add(new_record)
 
          if current_price <= product.target_price: 
            if current_price != last_price: 
              print("Deal Found!, Sending email for ", product.name)
              send_price_alert(product.name, current_price, product.user_email)
            else: 
              print("Price is still low but has not changed, no email sent")
          else: 
            print("No deal. Current Price: $", current_price, " Target price: $", product.target_price)

      except Exception as error: 
        print("Error checking ", product.name, ":", error)
        continue 

      session.commit()
      print("Update finished")


if __name__ == "__main__":
  while True: 
    try:
      update_prices()
    except Exception as error: 
      print("Error in loop", error)

      print("Waiti ng 6 hours for the next check")
      time.sleep(21600)