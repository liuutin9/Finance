# 初始化總金額，並從使用者輸入金額
total = int(input('How much money do you have? '))

# 初始化一個空列表，用來存放所有的項目（每個項目是一個 (描述, 金額) 的元組）
items = []

# 檢視紀錄函式，輸出所有的交易紀錄
def viewRecord():
    description_width = 20  # 項目描述欄位的寬度
    amount_width = 6        # 金額欄位的寬度
    outputRows = []         # 用來存放要輸出的每一行
    # 添加表頭
    outputRows.append("Description".ljust(description_width) + " Amount".ljust(amount_width))
    # 添加分隔線
    outputRows.append('=' * description_width + ' ' + '=' * amount_width)
    # 遍歷每個項目，並將其格式化後添加到輸出行
    for item in items:
        outputRows.append(item[0].ljust(description_width) + ' ' + item[1].ljust(amount_width))
    # 再次添加分隔線
    outputRows.append('=' * description_width + ' ' + '=' * amount_width)
    # 輸出當前的總金額
    outputRows.append(f'Now you have {total} dollars.')
    # 將所有行合併成字串，並輸出
    print('\n'.join(outputRows))
    return

# 添加紀錄函式，處理新增的收入或支出項目
def addRecord(newItems):
    delta = 0  # 記錄金額的變動值
    # 遍歷新增的每個項目
    for newItem in newItems:
        newItem = newItem.split(' ')
        items.append(newItem)  # 將項目添加到列表中
        delta += int(newItem[1])           # 計算總金額的變動
    return delta  # 返回金額變動

# 查找要刪除的紀錄，返回找到的紀錄數量
def findTrashRecord(trashItem):
    totalFound = 0  # 記錄找到的項目數
    offset = 0      # 偏移量，用來遍歷 items 列表
    # 遍歷 items 並查找與 trashItem 匹配的項目
    while (trashItem in items[offset:]):
        idx = items.index(trashItem, offset)  # 查找匹配的項目索引
        totalFound += 1  # 記錄找到的項目數
        offset = idx + 1  # 更新偏移量
    return totalFound  # 返回找到的項目總數

# 刪除紀錄函式，處理刪除項目的邏輯
def deleteRecord(trashItems):
    delta = 0  # 記錄金額的變動值
    # 遍歷要刪除的每個項目
    for trashItem in trashItems:
        trashItem = trashItem.split(' ')  # 將項目描述與金額拆開
        totalFound = findTrashRecord(trashItem)  # 查找該項目出現的次數
        numOfDelete = 1  # 預設只刪除一個項目
        # 如果找到超過一個相同的項目，詢問使用者要刪除多少個
        if (totalFound > 1):
            numOfDelete = int(input(f"{totalFound} '{trashItem[0]} {trashItem[1]}' have been found.\nHow many do you want to delete? "))
        # 刪除指定數量的項目
        for i in range(numOfDelete):
            if (trashItem in items):
                items.remove(trashItem)  # 從列表中移除項目
                delta += int(trashItem[1])           # 計算金額的變動
    return delta  # 返回金額變動

# 主程式循環，根據使用者的輸入執行不同的操作
while (True):
    
    # 詢問使用者想要執行的操作
    op = input('What do you want to do (add / view / delete / exit)? ')
    
    # 如果使用者輸入 'exit'，則結束程式
    if op == 'exit':
        exit()
        
    # 如果使用者輸入 'add'，則執行添加紀錄
    elif op == 'add':
        newItems = input('Add an expense or income record with description and amount:\n').split(', ')
        total += addRecord(newItems)  # 更新總金額
        print('Add success!')  # 提示添加成功
    
    # 如果使用者輸入 'view'，則檢視當前紀錄
    elif op == 'view':
        viewRecord()
    
    # 如果使用者輸入 'delete'，則執行刪除紀錄
    elif op == 'delete':
        trashItems = input('Which record do you want to delete?\n(ex: breakfast -50, lunch -70, ...)\n').split(', ')
        total -= deleteRecord(trashItems)  # 更新總金額
    
    # 如果使用者輸入的操作無效，則提示操作未定義
    else:
        print('Undefined operation')
