import requests
from bs4 import BeautifulSoup
import json
from openpyxl import load_workbook
import datetime

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
    
def get_exchange_rate_USD():
    url = "https://rate.bot.com.tw/xrt/flcsv/0/day"
    response = requests.get(url)
    response.encoding = 'utf-8'
    rows = response.text.split('\n')
    rate = rows[1].split(',')[13]  # Assuming the rate is in the 13th column
    return float(rate)


wb = load_workbook("帳目表.xlsx")

# 股票代碼
stock_symbols = ["006208.TW", "2890.TW", "VT"]

# 獲取股價
stock_prices = {}

# modify excel file
for symbol in stock_symbols:
    if (symbol[len(symbol)-3] == '.'):
        stockPrice = get_stock_price(symbol)
        wb[symbol]["C3"].value = stockPrice
    else:
        wb[symbol]["H3"].value = get_stock_price(symbol)
        
wb["投資"]["G2"].value = get_exchange_rate_USD()
    
wb.save("帳目表.xlsx")
wb.close()

now = datetime.datetime.now().replace(microsecond = 0)

log = open("log.txt", mode = "w")
log.write(f"{str(now)}\n")
log.write("Success!\n")
log.close()

print(now)
print("Success!")
