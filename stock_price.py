import requests
from bs4 import BeautifulSoup
import json
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
    url = 'https://mma.sinopac.com/ws/share/rate/ws_exchange.ashx'

    headers = {
        'Authorization': 'Bearer your_api_key',
    }

    params = {
        'Lang': 'zh-TW',
        'Currency': 'USD',
    }
    
    response = requests.get(url, headers=headers, params=params)
    data = json.loads(response.content)
    
    return float(data[0]['SubInfo'][0]['DataValue2'])

# 股票代碼
stock_symbols = ["006208.TW", "00692.TW", "00878.TW", "2890.TW", "2891.TW", "BND", "VT"]

# 獲取股價
stock_prices = {}

log = open("stock_price.txt", mode = "w")

# modify excel file
for symbol in stock_symbols:
    stockPrice = get_stock_price(symbol)
    log.writelines(f"{symbol},{stockPrice}\n")

log.close()

now = datetime.datetime.now().replace(microsecond = 0)

print(now)
print("Success!")

