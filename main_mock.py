import requests
import lxml
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.header import Header

url = "https://www.amazon.ca/DJI-Mini-Fly-More-Combo/dp/B08JGX61H7/ref=sr_1_5?dchild=1&keywords=dji+mavic+mini+2&qid=1615649389&sr=8-5"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, "lxml")
print(soup.prettify())

price = soup.find(id="priceblock_ourprice").get_text()
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)
print(price_as_float)

title = soup.find(id="productTitle").get_text().strip()
print(title)

BUY_PRICE = 740

if price_as_float < BUY_PRICE:
    message = MIMEText(f"{title} is now {price}", _charset="UTF-8")
    message['Subject'] = Header(f"Subject:Amazon Price Alert!\n\n{message}\n{url}", "utf-8")
    with smtplib.SMTP("YOUR_SMTP_ADDRESS") as connection:
        connection.starttls()
        result = connection.login("YOUR_EMAIL", "YOUR_PASSWORD")
        connection.sendmail(
            from_addr="YOUR_EMAIL",
            to_addrs="YOUR_EMAIL",
            msg=message.as_string()
        )