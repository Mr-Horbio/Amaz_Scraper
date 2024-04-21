import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import random
import pyfiglet
from termcolor import colored

# Render the text in ASCII art
ascii_text = pyfiglet.figlet_format("Garuda")

# Customize the color
colored_text = colored(ascii_text, color="green")

# Print the colored ASCII art text
print(colored_text)

# User-Agent headers
agents = {
    "User-Agent": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"
]
 
}

# Randomly choose a User-Agent
Headers = {"User-Agent": random.choice(agents["User-Agent"])}

# Function for sending request to amazon.in
def amazon_data():
    # Http Request
    webpage = requests.get(url, headers=Headers)
    # Soup Object containing all data
    soup = bs(webpage.content, "html.parser")
    # fetch links as list of Tag objects
    links = soup.find_all("a", attrs={"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
    # Store the links
    links_list = []
    # loop for extracting the link
    for link in links:
        links_list.append(link.get('href'))
    # Dictionary to store title, rating, price, and more details
    data = {"title": [], "price": [], "rating": []}
    # loop for extracting the product details
    for link in links_list:
        if not link.startswith("http") and not link.startswith("https"):
            # Send a get request to each individual product page
            single_product = requests.get("https://amazon.in" + link, headers=Headers)
            # create a soup object for every product page
            sp = bs(single_product.content, "html.parser")
            # add the title of the product in dictionary
            print("--------------------------")
            data['title'].append(get_title(sp))
            data['price'].append(get_price(sp))
            data['rating'].append(get_rating(sp))
            print("--------------------------")
    # Save the data to a CSV file
    df = pd.DataFrame(data)
    df.to_csv(output, index=False)
    print("save successful....")


def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": "productTitle"}).text.strip()
        print(f"[Product]:{title}")
        return title
    except Exception as e:
        return "----"


def get_rating(soup):
    try:
        rating = soup.find("span", attrs={"class": "a-icon-alt"}).text.strip()
        print(f"[Rating]:{rating}")
        return rating
    except Exception as e:
        return " -- "


def get_price(soup):
    try:
        price = soup.find("span", attrs={"class": "a-price-whole"}).text.strip()
        print(f"[Price]:{price}")
        return price
    except Exception as e:
        return " --- "


# Add URL of Amazon product list page
search = input("Please enter the product name: ")
search_formatted = search.replace(" ", "+")



url= f"https://www.amazon.in/s?k={search_formatted}"
output = input("Please enter the name of the output file[with .csv extension]: ")
if output == " ":
    output = "amazon.csv"

amazon_data()