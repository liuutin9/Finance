import json

def read_stock_repo():
    with open("stock_repo.txt", mode="r", encoding="utf-8") as stockRepoFileInput:
        stockRepo = json.load(stockRepoFileInput)
    return stockRepo

def update_stock_price(country:str, stock:str, price:float):
    stockRepo = read_stock_repo()
    if country == "US":
        stockRepo['US'][stock]['ClosingPrice'] = price
    elif country == "TW":
        stockRepo['TW'][stock]['ClosingPrice'] = price
    with open("stock_repo.txt", mode="w", encoding="utf-8") as stockRepoFile:
        json.dump(stockRepo, stockRepoFile, ensure_ascii=False, indent=4)