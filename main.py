import os
from bs4 import BeautifulSoup
import requests
import smtplib
import lxml
from dotenv import load_dotenv

load_dotenv()

url = "https://www.amazon.com/DualSense-Wireless-Controller-PlayStation-5/dp/B08FC6C75Y/ref=pd_rhf_d_gw_s_gcx-rhf_sccl_1_3/133-2815395-7321310?pd_rd_w=hlKA5&content-id=amzn1.sym.6954a684-f78d-4dab-ad79-1063555a011b&pf_rd_p=6954a684-f78d-4dab-ad79-1063555a011b&pf_rd_r=HAF2MY96NZJ1DKRBGZEK&pd_rd_wg=nC5l8&pd_rd_r=3d81bcf9-8e1c-43e9-809c-99ac38abaab6&pd_rd_i=B08FC6C75Y&psc=1"
headers={
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Accept-Language" : "en-US,en;q=0.9"
}

price_watch = 50.00

my_email = os.environ.get('EMAIL')
password = os.environ.get('APP_PASSWORD')
to_email = os.environ.get('TO_EMAIL')

#---------------------------------Scrapping the web ---------------------------#
def scrapping_web(url, headers):
    
    response = requests.get(url=url, headers=headers)
    track_web_page = response.content   
    soup = BeautifulSoup(track_web_page, "lxml")
    #print(soup.prettify())

    price_tag = (soup.find(name="span", class_="aok-offscreen"))
    price = price_tag.text.split("$")[1]
    price_float = float(price)
    #print(price_float)
    
    product_title = soup.select_one(selector="#productTitle").get_text(strip=True)
    #print(product_title)

    product_url = soup.find('link', {'rel': 'canonical'}).get('href')
    #print(product_url)
    
    return price_float, product_title, product_url

# ----------------------------- SEND EMAIL -----------------------------------#
def send_email(price, title, url):
    with smtplib.SMTP("smtp.gmail.com",port=587) as connection:
        # to secure our email connection
        connection.starttls()

        # log in to the email provider
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email, 
            to_addrs=to_email,
            msg=f"Subject:Amazon Price Alert!\n\n{title} is now ${price}\n{url}")

#--------------------Get Price, Product Title and Product URL------------#

(price, title, url) = scrapping_web(url, headers)

# -----------------Send Email if price is lower than expected price ----------

if price < price_watch:
    send_email(price, title, url)
