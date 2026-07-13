import json

def get_stock_repo():
    with open("stock_repo.txt", mode="r", encoding="utf-8") as stockRepoFileInput:
        stockRepo = json.load(stockRepoFileInput)
    return stockRepo

def get_stocks_tw():
    stockRepo = get_stock_repo()
    stocks = list(stockRepo['TW'].keys())
    return stocks

def get_stocks_us():
    stockRepo = get_stock_repo()
    stocks = list(stockRepo['US'].keys())
    return stocks

def get_stocks():
    stocks = {}
    stocks['TW'] = get_stocks_tw()
    stocks['US'] = get_stocks_us()
    return stocks

def update_stock_price(country:str, stock:str, current_price:float, yesterday_price:float = None):
    stockRepo = get_stock_repo()
    if country == "TW":
        stockRepo['TW'][stock]['CurrentPrice'] = current_price
        if yesterday_price is not None:
            stockRepo['TW'][stock]['YesterdayPrice'] = yesterday_price
    elif country == "US":
        stockRepo['US'][stock]['CurrentPrice'] = current_price
        if yesterday_price is not None:
            stockRepo['US'][stock]['YesterdayPrice'] = yesterday_price
    with open("stock_repo.txt", mode="w", encoding="utf-8") as stockRepoFile:
        json.dump(stockRepo, stockRepoFile, ensure_ascii=False, indent=4)