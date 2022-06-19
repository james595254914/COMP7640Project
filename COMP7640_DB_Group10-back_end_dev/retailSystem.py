import os
from tabulate import tabulate
from Shop import Shop
from Order import Order
from Item import Item


class retailSystem:

    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.shop = Shop()
        self.order = Order()
        self.item = Item()

        self.all_shop = None
        self.all_item = {}
        self.all_shop = self.shop.showAll()

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def printTopBar(self):
        self.clear()
        print('Customer ID: ', self.customer_id)
        print('--------------------------------------------------------------------------')
        print('\n\n\n')

    def printMainMenu(self):
        self.printTopBar()
        print('Input the number to select:')
        print('1 Shop Management')
        print('2 Item Management')
        print('3 Item Search')
        print('4 Item Purchase')
        print('5 Order canceling')

    # Shop Management

    def printShopMenu(self):
        self.printTopBar()
        print('1 Show all shops')
        print('2 Add a new shop to the database')

    def showAllShops(self, listOnly = False):
        self.printTopBar()
        #get shop list API
        self.all_shop = self.shop.showAll()
        headers=["ID","Name", "Rating", "Location"]
        print(tabulate(self.all_shop, headers, tablefmt="pretty"))
        # print(self.all_shop[1][0])
        if not listOnly:
            input("Press Enter to continue")

    def addNewShop(self):
        new_shop = {}

        self.printTopBar()
        print('You are adding a new shop!\n')
        new_shop['name'] = str(input('Please enter the shop name: '))
        new_shop['rating'] = str(input('Please enter the shop rating: '))
        new_shop['location'] = str(input('Please enter the shop location: '))

        # print('new_shop: ', new_shop, '\n')
        #addshop API
        rt = self.shop.addOne(new_shop['name'], new_shop['rating'], new_shop['location'])
        if rt :
            print('Shop added successfully!')
            print('Press 1 to view all shops or Press Enter to go back main menu')
            selection = str(input('Selection: '))
            if selection == '1':
                self.showAllShops()
        else:
            input("Press Enter to continue")

    # Item Management

    def printItemMenu(self):
        self.printTopBar()
        print('1 Show all items of a shop')
        print('2 Add a new item to the shop')

    def showShopItems(self, listOnly = True, shop_id = None):
        if shop_id == None:
            self.printTopBar()
            self.showAllShops(True)
            shop_id = int(input('Please select a shop [integer]: S'))
            print('\n')
        #get shop items list API
        shop_items = self.item.listAllItemByShop('S'+str(shop_id))
        self.all_item[shop_id] = shop_items
        if len(shop_items) > 0:
            headers=["ID", "Shop", "Name", "price", "keyword 1", "keyword 2", "keyword 3", "Available Quantity"]
            print(tabulate(shop_items, headers, tablefmt="pretty"))
        else:
            print('No item found')
        
        if listOnly:
            input("Press Enter to continue")
        else:
            item_id = int(input('Please select an item [integer]: I'))
            return {"shop_id":shop_id, "item_id":item_id}

    def addNewItem(self):
        new_item = {}

        self.printTopBar()
        print('You are adding a new item!\n')
        self.showAllShops(True)
        shop_id = str(input('Please select a shop [integer]: S'))
        new_item['name'] = str(input('Please enter the item name: '))
        new_item['price'] = input('Please enter the item price: $')
        new_item['qty'] = int(input('Please enter item''s initial quantity: '))
        new_item['kw1'] = ''
        new_item['kw2'] = ''
        new_item['kw3'] = ''
        for kw in range(3):
            input_kw = str(input('Please enter the item keyword: '))
            new_item['kw'+str(kw+1)] = input_kw
            selection = str(input('Input more keywords? [y/n]: '))
            if selection.lower() != 'y':
                break

        print('new_shop: ', new_item, '\n')
        # add new item API
        rt = self.item.addOne(new_item['name'], new_item['price'], new_item['qty'], 'S'+shop_id, new_item['kw1'], new_item['kw2'], new_item['kw3'])
        if rt :
            print('Item added successfully!')
            print('Press 1 to view all item in shop or Press Enter to go back main menu')
            selection = str(input('Selection: '))
            if selection == '1':
                self.showShopItems(True, shop_id)
        else:
            input("Press Enter to continue")

    # Item Search

    def itemSearch(self):
        self.printTopBar()
        keyword = str(input('Keyword: '))
        rt = self.item.search(keyword)
        headers = ["ID", "Name", "Price", "Available Quantity", "Shop"]
        if rt :
            print(tabulate(rt, headers, tablefmt="pretty"))
        else:
            print('No result')
        input("Press Enter to continue")

    # Item purchase

    def itemPurchase(self):
        self.printTopBar()
        shop_list = []
        item_list = []
        qty_list = []
        headers=["Shop","Item", "Quantity"]
        order_table = []
        selection = '1'
        while selection == '1':
            rt = self.showShopItems(False)
            qty_ok = False
            while qty_ok == False:
                stock_qty = self.order.itemQuantity('S'+str(rt['shop_id']), 'I'+str(rt['item_id']))
                qty = int(input('Please enter the required quantity: '))
                if int(stock_qty) >= qty:
                    qty_ok = True
                else:
                    print('Invaild quantity')

            shop_list.append('S'+str(rt['shop_id']))
            item_list.append('I'+str(rt['item_id']))
            qty_list.append(qty)
            item_name = [tup for tup in self.all_item[rt['shop_id']] if tup[0] == 'I'+str(rt['item_id'])][0][2]
            order_table.append([self.all_shop[rt['shop_id']-1][1], item_name, qty])
            
            print(tabulate(order_table, headers, tablefmt="pretty"))
            print('Press 1 to add more items or Press Enter submit order')
            selection = str(input('Selection: '))
        
        new_oid = self.order.addMultiple(self.customer_id, shop_list, item_list, qty_list)
        if new_oid :
            print('Order placed successfully. Order ID: ' + new_oid)
            input('Press Enter to go back main menu')
        else:
            input("Press Enter to continue")

    # Order canceling

    def orderCanceling(self):
        self.printTopBar()
        
        print('1. Cancel whole order')
        print('2. Cancel item(s) in order\n')
        selection = str(input('Selection: '))

        orders = self.order.getOrdersByUser(self.customer_id)
        orders = list(orders)

        if orders:
            order_table = []
            for order in orders:
                order = order[0]
                order_items_details = self.order.getItemsByOrder(order, self.customer_id)
                item_names = [a_tuple[2] for a_tuple in order_items_details]
                item_names = ' '.join([str(elem) for elem in item_names])
                order_table.append([order, item_names])
            
            headers = ["ID", "Items"]
            print(tabulate(order_table, headers, tablefmt="pretty"))
            if selection == '1': #cancel whole order
                order_id = int(input('Please select an order [integer]: O'))
                rt = self.order.removeOrder('O'+str(order_id))
                if rt == True:
                    print('Order '+'O'+str(order_id)+' canceled successfully!')
            elif selection == '2':
                order_id = int(input('Please select an order [integer]: O'))
                order_items = self.order.getOrders(self.customer_id, 'O'+str(order_id))
                order_items = list(order_items)
                headers = ['Index', 'Shop', 'Item', 'price', 'Quantity', 'Sub-total']
                continue_cancel = True
                while continue_cancel == True:
                    order_item_table = []
                    for idx, item in enumerate(order_items):
                        if int(item[2][1]) not in self.all_item:
                            shop_items = self.item.listAllItemByShop('S'+str(int(item[2][1])))
                            self.all_item[int(item[2][1])] = shop_items
                        item_name = [tup for tup in self.all_item[int(item[2][1])] if tup[0] == 'I'+item[3][1]][0][2]
                        order_item_table.append([ idx+1 , self.all_shop[int(item[2][1])-1][1], item_name, item[4], item[5], item[6] ])
                    print(tabulate(order_item_table, headers, tablefmt="pretty"))
                    item_to_del = int(input('Please select an item [index]: '))
                    rt = self.order.removeItem('O'+str(order_id), order_items[item_to_del-1][3], order_items[item_to_del-1][2])
                    if rt == True:
                        del order_items[item_to_del-1]
                        print('Item canceled successfully!')
                        if len(order_items) == 0:
                            print('No more item in this order!')
                            continue_cancel = False
                        else:
                            selection = str(input('Cancel more item? [y/n]: '))
                            if selection.lower() != 'y':
                                order_item_table = []
                                for idx, item in enumerate(order_items):
                                    if int(item[2][1]) not in self.all_item:
                                        shop_items = self.item.listAllItemByShop('S'+str(int(item[2][1])))
                                        self.all_item[int(item[2][1])] = shop_items
                                    item_name = [tup for tup in self.all_item[int(item[2][1])] if tup[0] == 'I'+item[3][1]][0][2]
                                    order_item_table.append([ idx+1 , self.all_shop[int(item[2][1])-1][1], item_name, item[4], item[5], item[6] ])
                                print(tabulate(order_item_table, headers, tablefmt="pretty"))
                                continue_cancel = False
                    else:
                        print('Remove item failed')
                        continue_cancel = False
        else:
            print('No order found')
        input("Press Enter to continue")
