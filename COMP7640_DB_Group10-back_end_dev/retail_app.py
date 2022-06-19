import sys
from retailSystem import retailSystem
from Customer import Customer
from tabulate import tabulate
import os

def main():

    customer_id = 'C1' #default
    os.system('cls' if os.name == 'nt' else 'clear')
    cus = Customer()
    print('1. Contiune as existing customer')
    print('2. Create new customer')
    user_select = str(input('Selection: '))
    if user_select == '1':
        cus_list = cus.showAll()
        headers=["ID", "Tel.", "Address"]
        print(tabulate(cus_list, headers, tablefmt="pretty"))
        customer_id = str(input('Please select a customer [integer]: C'))
        customer_id = 'C'+customer_id
    else:
        new_cus_tel = str(input('Please enter your telephone: '))
        new_cus_address = str(input('Please enter your address: '))
        customer_id = cus.addOne(new_cus_tel, new_cus_address)
        if customer_id == False:
            print('create customer failed. Contiune as C1')
            customer_id = 'C1'

    rs = retailSystem(customer_id)

    while True:
        rs.printMainMenu()
        selection = str(input('Selection: '))

        if selection == '1':  # Shop Management
            rs.printShopMenu()
            selection = str(input('Selection: '))
            if selection == '1':
                rs.showAllShops()
            elif selection == '2':
                rs.addNewShop()

        elif selection == '2':  # Item Management
            rs.printItemMenu()
            selection = str(input('Selection: '))
            if selection == '1':
                rs.showShopItems()
            elif selection == '2':
                rs.addNewItem()

        elif selection == '3':  # Item Search
            rs.itemSearch()

        elif selection == '4':  # Item purchase
            rs.itemPurchase()

        elif selection == '5':  # Item purchase
            rs.orderCanceling()


if __name__ == '__main__':
    main()
