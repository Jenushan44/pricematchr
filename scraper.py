import httpx
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

def get_price(url: str): 

    api_key = os.getenv("SCRAPER_API_KEY") 
    api_url = "http://api.scraperapi.com?api_key=" + api_key + "&url=" + url    
    
    try: 
        response = httpx.get(api_url, timeout = 60.0)  # takes the url and retrieves the status code, headers and html
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser") # organizes the HTML string (response.txt) into a searchable map
            
            main_container = soup.find("div", id="corePrice_feature_div") or soup.find("div", id="apex_desktop") or soup.find("div", id="centerCol") # searches html code for div's that contain prices
            if main_container:
                # splits the amazon price into dollars and cents
                whole = main_container.find("span", class_="a-price-whole")
                fraction = main_container.find("span", class_="a-price-fraction")
                if whole and fraction: 
                    amazon_price = whole.text.replace(".", "").strip() + "." + fraction.text.strip()
                    found_price = float(amazon_price)
                    print("Found price: $", found_price)
                    return found_price      
        else: 
            print("Failed to get price: ", {response.status_code})
            return None 
    except Exception as error:
        print("Error: ", error)
        return None 