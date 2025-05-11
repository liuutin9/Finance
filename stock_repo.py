import requests
from bs4 import BeautifulSoup
import json
import datetime

# Dictionary to store stock prices by country
stockPrices = {'TW': {}, 'US': {}}

# Function to fetch stock price for US stocks
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

# Function to get the exchange rate for USD
def get_exchange_rate_USD():
    url = 'https://mma.sinopac.com/ws/share/rate/ws_exchange.ashx'
    headers = {
        'Authorization': 'Bearer your_api_key',  # Replace 'your_api_key' with actual API key
    }
    params = {
        'Lang': 'zh-TW',
        'Currency': 'USD',
    }
    
    response = requests.get(url, headers=headers, params=params)
    data = json.loads(response.content)
    
    return float(data[0]['SubInfo'][0]['DataValue2'])

# Load the stock repository from file
with open("stock_repo.txt", mode="r", encoding="utf-8") as stockRepoFileInput:
    stockRepo = json.load(stockRepoFileInput)

# Combine stocks from both Taiwan (TW) and US into one list
stocks = [*(stockRepo['TW'])] + [*(stockRepo['US'])]

# Get the USD exchange rate
exchangeRateUSD = get_exchange_rate_USD()

# Iterate through the stocks to fetch their prices
for stock in stocks:
    if stock[0].isalpha():  # US stock (alpha symbol)
        stockPrice = float(get_stock_price(stock))
        stockPrice *= exchangeRateUSD  # Convert to local currency
        stockRepo['US'][stock]['ClosingPrice'] = stockPrice
    else:  # Taiwan stock (numeric symbol)
        stockPrice = float(get_stock_price(stock + ".TW"))
        stockRepo['TW'][stock]['ClosingPrice'] = stockPrice

# Save updated stock repository back to file
with open("stock_repo.txt", mode="w", encoding="utf-8") as stockRepoFile:
    json.dump(stockRepo, stockRepoFile, ensure_ascii=False, indent=4)

# Log the update time
with open("stock_repo_log.txt", mode="w", encoding="utf-8") as log:
    now = datetime.datetime.now().replace(microsecond=0)
    print(now, file=log)
    print(now)
    print("Stock Repo Update Success!")
