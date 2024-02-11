import requests
from bs4 import BeautifulSoup
import csv

def get_stock_price(symbol):
    url = f"https://tw.finance.yahoo.com/quote/{symbol}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find("div", {"class": "D(f) Ai(fe) Mb(4px)"}).find("span")
        if price_element:
            return price_element.text
        else:
            return "Price not found"
    else:
        return "Failed to fetch data"

# 股票代碼
stock_symbols = ["006208.TW", "00692.TW", "00878.TW", "2890.TW", "BND", "VEA", "VT", "VTI"]

# 獲取股價
stock_prices = []

for symbol in stock_symbols:
    stock_prices.append(get_stock_price(symbol))
    
# 寫入 txt 檔
out = open("stock_prices.txt", mode = "w")
for i in range(len(stock_symbols)):
    out.write(f"{stock_symbols[i]},{stock_prices[i]}\n")
out.close()

print("股價已成功寫入 stock_prices.txt 檔案中.")
