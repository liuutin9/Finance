import sys
import os
import pandas as pd
from datetime import datetime
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# 嘗試讀取紀錄檔案，若不存在則初始化並要求輸入總金額
def initialize():
    try:
        record = open('records.txt', 'r')
        file_size = os.path.getsize('records.txt')
        if file_size == 0:
            raise FileNotFoundError
        initialValue, total = record.readline().split(',')
        initialValue = int(initialValue)
        total = int(total)
        data = record.read().split('\n')[1:-1]
        data = [x.split(',') for x in data]
        df = pd.DataFrame(data, columns=['Description', 'Amount', 'Date'])
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')  # 將 Amount 轉換為數字格式
        record.close()
        print('Welcome back! You have', total + initialValue, 'dollars.')
    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        sys.stderr.write(f"Creating a new record.txt...\n")
        print('Welcome to your personal finance tracker!')
        while (True):
            try:
                initialValue = int(input('Please enter your initial total amount of money: '))
                break
            except ValueError:
                sys.stderr.write("Error: Invalid input format. Please enter an integer.\n")

        total = initialValue
        df = pd.DataFrame(columns=['Description', 'Amount', 'Date'])
    return df, initialValue


def view(df:pd.DataFrame, initialValue:int) -> None:
    '''
    View the records in the dataframe
    Args:
        df: pandas.DataFrame
        initialValue: int (initial total amount of money)
    Returns:
        None
    '''
    total = df['Amount'].sum() + initialValue
    description_width = 20
    amount_width = 8
    date_width = 12

    # ANSI escape codes for coloring
    HEADER_COLOR = '\033[36m'
    ROW_COLOR_POS = '\033[91m' 
    ROW_COLOR_NEG = '\033[92m'
    TOTAL_COLOR_NORMAL = '\033[0m'
    TOTAL_COLOR_WARNING = '\033[93m'
    RESET_COLOR = '\033[0m'

    # Characters for the solid line border
    top_left = "┌"
    top_right = "┐"
    bottom_left = "└"
    bottom_right = "┘"
    horizontal = "─"
    vertical = "│"
    
    # Calculate the width of the table
    table_width = description_width + amount_width + date_width + 6  # +4 for the spaces, separators and paddings
    
    # Create top border
    outputRows = [top_left + horizontal * table_width + top_right]
    
    # Header
    header = (HEADER_COLOR + "Description".center(description_width) + '  ' + 
              "Amount".center(amount_width) + '  ' + "Date".center(date_width) + RESET_COLOR)
    outputRows.append(vertical + ' ' + header + ' ' + vertical)
    
    # Separator between header and data
    outputRows.append(vertical + ' ' + '=' * description_width + '  ' + '=' * amount_width + '  ' + '=' * date_width + ' ' + vertical)
    
    # Data rows
    df_sorted = df.sort_values(by='Date')
    for _, row in df_sorted.iterrows():
        ROW_COLOR = ROW_COLOR_POS if row['Amount'] > 0 else ROW_COLOR_NEG
        row_text = (ROW_COLOR + row['Description'].ljust(description_width) + '  ' +
                    str(row['Amount']).rjust(amount_width) + '  ' +
                    row['Date'].strftime('%Y-%m-%d').center(date_width) + RESET_COLOR)
        outputRows.append(vertical + ' ' + row_text + ' ' + vertical)
    
    # Bottom separator
    outputRows.append(vertical + ' ' + '=' * (table_width - 2) + ' ' + vertical)
    
    # Total row
    TOTAL_COLOR = TOTAL_COLOR_NORMAL if total >= 0 else TOTAL_COLOR_WARNING
    total_row = (TOTAL_COLOR + f'Now you have {total} dollars.'.center(table_width) + RESET_COLOR)
    outputRows.append(vertical + total_row + vertical)
    
    # Create bottom border
    outputRows.append(bottom_left + horizontal * table_width + bottom_right)
    
    # Print everything
    print('\n'.join(outputRows))



def add(df:pd.DataFrame, newItems:list) -> pd.DataFrame:
    '''
    Add a new record to the dataframe
    Args:
        df: pandas.DataFrame
        newItems: list of [description, amount, date]
    Returns:
        pandas.DataFrame (updated dataframe)
    '''
    try:
        for newItem in newItems:
            description, amount, dateStr = newItem.split(' ')
            date = datetime.strptime(dateStr, '%Y-%m-%d')
            # date_now = datetime.now()  # 紀錄當前時間
            new_df = pd.DataFrame([[description, int(amount), date]], columns=['Description', 'Amount', 'Date'])
            df = pd.concat([df, new_df], ignore_index=True)
            print('Add success!')
    except ValueError:
        sys.stderr.write("Error: Invalid input format. Please use 'description amount date(yyyy-mm-dd)'.\n")
    return df

def findTrashRecord(df:pd.DataFrame, trashItem:list) -> int:
    '''
    Return the number of records found in the dataframe
    Args:
        df: pandas.DataFrame
        trashItem: [description, amount, date]
    Returns:
        int (number of records found)
    '''
    # print(df['Description'] == trashItem[0])
    return df[(df['Description'] == trashItem[0]) & (df['Amount'] == int(trashItem[1])) & (df['Date'] == trashItem[2])].shape[0]

def delete(df:pd.DataFrame, trashItems:list) -> pd.DataFrame:
    '''
    Delete the records in the dataframe
    Args:
        df: pandas.DataFrame
        trashItems: [description, amount, date]
    Returns:
        pandas.DataFrame (updated dataframe)
    '''
    try:
        for trashItem in trashItems:
            description, amount, dateStr = trashItem.split(' ')
            date = datetime.strptime(dateStr, '%Y-%m-%d')
            totalFound = findTrashRecord(df, [description, amount, date])
            if totalFound == 0:
                print(f"No '{description} {amount} {dateStr}' found.")
                continue
            numOfDelete = 1
            if totalFound > 1:
                numOfDelete = int(input(f"{totalFound} '{description} {amount}' found.\nHow many do you want to delete? "))
            for _ in range(numOfDelete):
                idx = df[(df['Description'] == description) & (df['Amount'] == int(amount)) & (df['Date'] == date)].index
                if len(idx) > 0:
                    df = df.drop(idx[0])
        df.reset_index(drop=True, inplace=True)
    except ValueError:
        sys.stderr.write("Error: Invalid input format. Please use 'description amount date(yyyy-mm-dd)'.\n")
    return df

def save(df:pd.DataFrame, initialValue:int) -> None:
    '''
    Save the records to a file
    Args:
        df: pandas.DataFrame
        initialValue: int (initial total amount of money)
    Returns:
        None
    '''
    csvFile = str(df.to_csv(index=False))
    with open('records.txt', 'w', newline='') as f:
        f.write(f'{initialValue},{df['Amount'].sum()}\n')
        f.write(csvFile)

# 主程式循環
def main():
    df, initialValue = initialize()
    while True:
        try:
            op = input('What do you want to do (add / view / delete / exit)? ')
            if op == 'exit':
                save(df, initialValue)
                print('Records saved to file. Exiting...')
                exit()
            elif op == 'add':
                newItems = input('Add an expense or income record with description and amount:\n(description, amount, yyyy-mm-dd)\n').split(', ')
                df = add(df, newItems)
            elif op == 'view':
                view(df, initialValue)
            elif op == 'delete':
                trashItems = input('Which record do you want to delete?\n').split(', ')
                df = delete(df, trashItems)
            else:
                raise ValueError('Invalid command. Try again.')
        except Exception as e:
            sys.stderr.write(f"An error occurred: {e}\n")

if __name__ == "__main__":
    main()
