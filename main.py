total = int(input('How much money do you have? '))
newItem = input('Add an expense or income record with description and amount:\n').split(' ')
newItem[1] = int(newItem[1])
total += newItem[1]
print(f'Now you have {total} dollars.')