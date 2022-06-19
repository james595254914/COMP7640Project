import sys
import os

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def printTopBar():
    clear()
    print('Customer ID: ', customer_id)
    print('--------------------------------------------------------------------------')
    print('\n\n\n')

def printMainMenu():
    printTopBar()
    print('Input the number to select:')
    print('1 Shop Management')
    print('2 Item Management')
    print('3 Item Search')
    print('4 Item Purchase')
    print('5 Order canceling')

#Shop Management
def printShopMenu():
    printTopBar()
    print('1 Show all shops')
    print('2 Add a new shop to the database')

def showAllShops():
    printTopBar()
    print('in showAllShops')
    input("Press Enter to continue")

def addNewShop():
    printTopBar()
    print('in addNewShop')
    input("Press Enter to continue")

#Item Management
def printItemMenu():
    printTopBar()
    print('1 Show all items of a shop')
    print('2 Add a new item to the shop')

def showShopItems():
    printTopBar()
    print('in showShopItems')
    input("Press Enter to continue")

def addNewItem():
    printTopBar()
    print('in addNewItem')
    input("Press Enter to continue")

#Item Search
def itemSearch():
    printTopBar()
    print('in itemSearch')
    keyword = str(input('Keyword: '))
    input("Press Enter to continue")

#Item purchase
def itemPurchase():
    printTopBar()
    print('in itemPurchase')
    input("Press Enter to continue")

#Order canceling
def orderCanceling():
    printTopBar()
    print('in orderCanceling')
    input("Press Enter to continue")

def main():
    global customer_id
    try: 
        customer_id = sys.argv[1]
    except IndexError:
        customer_id = 1

    while True:
        printMainMenu()
        # selection = ''
        # while selection not in ['1', '2', '3', '4', '5']:
        selection = str(input('Selection: '))

        
        if selection == '1': #Shop Management
            printShopMenu()
            selection = str(input('Selection: '))
            if selection == '1':
                showAllShops()
            elif selection == '2':
                addNewShop()

        elif selection == '2': #Item Management
            printItemMenu()
            selection = str(input('Selection: '))
            if selection == '1':
                showShopItems()
            elif selection == '2':
                addNewItem()

        elif selection == '3': #Item Search
            itemSearch()

        elif selection == '4': #Item purchase
            itemPurchase()

        elif selection == '5': #Item purchase
            orderCanceling()
if __name__ == '__main__':
    main()