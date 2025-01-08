import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

asimov_url = "https://www.amazon.ca/Complete-Asimovs-Foundation-Foundations-Prelude/dp/B01EFDEMS8/ref=pd_sbs_d_sccl_2_1/141-8104449-9414219?pd_rd_w=6ewdN&content-id=amzn1.sym.4b791088-03f0-49af-8af1-ae2f52d6208b&pf_rd_p=4b791088-03f0-49af-8af1-ae2f52d6208b&pf_rd_r=Z3TYEZXTMJS25BTPXCE7&pd_rd_wg=oJNRl&pd_rd_r=b2e02e2c-56ed-4c69-ba58-df0c331d297a&pd_rd_i=B01EFDEMS8&psc=1"
headers = {
    #"Request Line": "GET / HTTP/1.1",
    #"Host": "myhttpheader.com",
    "Cookie": "PHPSESSID=732fb6ea409c93fc38d058d6f81ce8cf; _ga=GA1.2.1080859464.1714240104; _gid=GA1.2.505964109.1714240104; _gat=1; _ga_VL41109FEB=GS1.2.1714240104.1.0.1714240104.0.0.0",
    "Accept-Language": "en-US,en;q=0.9,fr;q=0.8,fr-FR;q=0.7,en-CA;q=0.6,en-GB;q=0.5",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
}

response = requests.get(url=asimov_url, headers=headers)
asimov_page = response.text

soup = BeautifulSoup(asimov_page, "lxml")
price_num = soup.find(name="span", class_="a-price-whole")
price_cents = soup.find(name="span", class_="a-price-fraction")
price = float(price_num.get_text() + price_cents.get_text())
print(price)

import smtplib
my_email = os.getenv('SENDER_EMAIL')
password = os.getenv('PASSWORD')
email = os.getenv('RECEIVER_EMAIL')

threshold = 76

if price < threshold:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=email,
                            msg=f"The price is right!\n\n The whole foundation series is below $80\n "
                                f"Here is a link to it: {asimov_url}")
