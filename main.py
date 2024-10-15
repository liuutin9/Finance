import sys
import pandas as pd
from datetime import datetime
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# 嘗試讀取紀錄檔案，若不存在則初始化並要求輸入總金額
def initialize():
    try:
        df = pd.read_csv('records.txt', parse_dates=['Date'])
        print('Welcome back!')
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df = pd.DataFrame(columns=['Description', 'Amount', 'Date'])
        print('Welcome to your personal finance tracker!')
    return df

def view(df):
    total = df['Amount'].sum()
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
    outputRows.append(vertical + ' ' + '=' * description_width + '  ' + '=' * amount_width + '  ' + '=' * date_width + ' ' + vertical)
    
    # Total row
    TOTAL_COLOR = TOTAL_COLOR_NORMAL if total >= 0 else TOTAL_COLOR_WARNING
    total_row = (TOTAL_COLOR + f'Now you have {total} dollars.'.center(table_width) + RESET_COLOR)
    outputRows.append(vertical + total_row + vertical)
    
    # Create bottom border
    outputRows.append(bottom_left + horizontal * table_width + bottom_right)
    
    # Print everything
    print('\n'.join(outputRows))



def add(df, newItems):
    try:
        for newItem in newItems:
            desc, amt = newItem.split(' ')
            date_now = datetime.now()  # 紀錄當前時間
            new_df = pd.DataFrame([[desc, int(amt), date_now]], columns=['Description', 'Amount', 'Date'])
            df = pd.concat([df, new_df], ignore_index=True)
    except ValueError:
        print("Error: Invalid input format. Please use 'description amount'.")
    return df

def findTrashRecord(df, trashItem):
    return df[(df['Description'] == trashItem[0]) & (df['Amount'] == int(trashItem[1]))].shape[0]

def delete(df, trashItems):
    try:
        for trashItem in trashItems:
            desc, amt = trashItem.split(' ')
            totalFound = findTrashRecord(df, [desc, amt])
            numOfDelete = 1
            if totalFound > 1:
                numOfDelete = int(input(f"{totalFound} '{desc} {amt}' found.\nHow many do you want to delete? "))
            for _ in range(numOfDelete):
                idx = df[(df['Description'] == desc) & (df['Amount'] == int(amt))].index
                if len(idx) > 0:
                    df = df.drop(idx[0])
        df.reset_index(drop=True, inplace=True)
    except ValueError:
        print("Error: Invalid input format. Please use 'description amount'.")
    return df

# 主程式循環
def main():
    df = initialize()
    while True:
        try:
            op = input('What do you want to do (add / view / delete / exit)? ')
            if op == 'exit':
                df.to_csv('records.txt', index=False)
                print('Records saved to file. Exiting...')
                exit()
            elif op == 'add':
                newItems = input('Add an expense or income record with description and amount:\n').split(', ')
                df = add(df, newItems)
                print('Add success!')
            elif op == 'view':
                view(df)
            elif op == 'delete':
                trashItems = input('Which record do you want to delete?\n').split(', ')
                df = delete(df, trashItems)
            else:
                print('Invalid command. Try again.')
        except Exception as e:
            sys.stderr.write(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
