from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas
import argparse
import random
import requests
import pyfiglet

text = "SCRAPER"
ascii_art = pyfiglet.figlet_format(text)
print(ascii_art)




#--------------------------------------------------Amazon Scraper--------------------------------------------#

def amazon(Keyword):
    response = requests.get("http://google.com/")
    if response.status_code==200:
        print("Connected to the internet")
    else:
        print("Not Connected to the internet")  
        
    chrome_options = Options()
    chrome_options.add_argument("--headless=True")
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(f"https://www.amazon.in/")
    print("Finding data......")
    browser.find_element(By.ID, "twotabsearchtextbox").send_keys(Keyword)
    browser.find_element(By.ID, "nav-search-submit-button").click()
    time.sleep(5)
    titles = browser.find_elements(By.XPATH, '//span[@class="a-size-medium a-color-base a-text-normal"]')
    prices = browser.find_elements(By.XPATH, '//span[@class="a-price-whole"]')
    

    data = {
        "titles": [],
        "prices": [],
    }

    for title, price in zip(titles, prices):
        data["titles"].append(title.text)
        data["prices"].append(price.text)
    print("creating file.......")
    file_name = str(random.randint(1000,5000))
    df = pandas.DataFrame(data,)
    df.to_csv(file_name+".csv",index=False)
    browser.close()
    print("File Created Successfully")
    print("File Name: ",file_name+".csv")

 


#-------------------------------Main Arguments SEction-----------------------------------------------------#

def main():
    parser = argparse.ArgumentParser(description="This Tool helps to get ecommerce product data",usage="%(prog)s [options] Keyword",epilog="%(prog)s -a laptop")
    parser.add_argument("-a",help="Scrap Data From Amazon",metavar = "amazon",dest="Amazon",nargs=1)
    parser.add_argument("-f",help="Scrap Data From Flipkart",metavar = "flipkart",dest="Flipkart",nargs=1)
    args = parser.parse_args()
   
    

    if args.Amazon:
        amazon(args.Amazon)
   
    
if __name__=="__main__":
    main()
