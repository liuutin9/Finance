import requests
from bs4 import BeautifulSoup
import json
import datetime

stockPrices = {'TW': {}, 'US': {}}

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
    
def get_taiwan_stock_price(stocks, stockRepo):
    url = f"https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_AVG_ALL"
    response = requests.get(url)
    data = json.loads(response.content)
    
    for stock in data:
        if stock['Code'] in stocks:
            stockRepo['TW'][stock['Code']]['ClosingPrice'] = float(stock['ClosingPrice'])
    
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

stockRepo = {}
stockRepoFileInput = open("stock_repo.txt", mode = "r", encoding = "utf-8")
stockRepo = json.load(stockRepoFileInput)
# stockRepoFileInputString = stockRepoFileInput.read().replace("'", '"')
# stockRepo = json.loads(stockRepoFileInputString)
stockRepoFileInput.close()

stocks = [*(stockRepo['TW'])] + [*(stockRepo['US'])]

stockRepoFile = open("stock_repo.txt", mode = "w", encoding = "utf-8")

exchangeRateUSD = get_exchange_rate_USD()

get_taiwan_stock_price(stocks, stockRepo)

for stock in stocks:
    if stock[0].isalpha():
        stockPrice = float(get_stock_price(stock))
        stockPrice *= exchangeRateUSD
        stockRepo['US'][stock]['ClosingPrice'] = stockPrice
    
print(str(stockRepo).replace("'", '"'), file = stockRepoFile)
    
stockRepoFile.close()

log = open("stock_repo_log.txt", mode = "w", encoding = "utf-8")
now = datetime.datetime.now().replace(microsecond = 0)
print(now, file = log)
print(now)
print("Stock Repo Update Success!")
log.close()
