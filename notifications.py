import os
import smtplib
from email.message import EmailMessage 
from dotenv import load_dotenv

load_dotenv()

def send_price_alert(product_name, price, user_email):
  sender_email = os.getenv("EMAIL_ADDRESS")
  sender_password = os.getenv("EMAIL_PASSWORD")
  
  message= EmailMessage()
  message["Subject"] = "Price Drop: ", product_name 
  message["From"] = sender_email 
  message["To"] = user_email 
  message.set_content("Alert: The price for ", product_name, "has dropped to $", price, ".")

  try: 
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
      smtp.login(sender_email, sender_password)
      
      smtp.send_message(message)
      print("Email sent to ", user_email)

  except Exception as error: 
    print("Email failed: ", error)