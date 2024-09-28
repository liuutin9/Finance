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
    
def get_taiwan_stock_price(stocks):
    url = f"https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_AVG_ALL"
    response = requests.get(url)
    data = json.loads(response.content)
    
    priceList = []
    
    for stock in data:
        if stock['Code'] in stocks:
            priceList.append(f"{stock['Name']},{stock['ClosingPrice']}")
    
    return priceList
    
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
stock_symbols = ["BND", "VT"]
stocks = ['006208', '00692', '00878', '2890', '2891']

# 獲取股價
stock_prices = {}

log = open("stock_price.txt", mode = "w", encoding = "utf-8")

exchangeRateUSD = get_exchange_rate_USD()

taiwanStockPriceList = get_taiwan_stock_price(stocks)

for stock in taiwanStockPriceList:
    print(stock, file = log)

# modify excel file
for symbol in stock_symbols:
    stockPrice = float(get_stock_price(symbol))
    stockPrice *= exchangeRateUSD
    print(f"{symbol},{stockPrice}", file = log)

log.close()

now = datetime.datetime.now().replace(microsecond = 0)

print(now)
print("Success!")

