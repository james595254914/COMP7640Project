# Introduction

# How to Run

### Install requirements

```bash
pip install -r requirements.txt
```
### Run the online retail database application

```bash
python retail_app.py
```
# How to use Shop.py

```
shop = Shop()
```

### return all shops

```
all_shops = shop.showAll()
```

### add a new shop

```
new_sid = shop.addOne('Computer Shop', 5, 'Mong Kok')
```

# How to use Item.py

```
item = Item()
```

### return all items of one shop

```
items_in_shop = item.listAllItemByShop('s1')
```

### add one item for one shop

```
new_iid = item.addOne('Banana', 3, 20, 'S1', 'Yellow', 'Delicious')
```

### search an item by the name or keyword of the  item

```
items = item.search('banana')
```

# How to use Order.py

```
order = Order()
```

### Get Orders by user

```
orders = order.getOrdersByUser(cid="C1")
```

### Get Items by order id

get items in the order by order id

```
orders = order.getItemsByOrder(oid="O2")
```

### item purchase

#### return the quantity of one item

```
item_qty = order.itemQuantity('S1', 'I2')
```

#### add one item purchase, return one-item order id

```
new_oid = order.addOne('C1', 'S1', 'I2', 2)
```

#### add multiple items purchase, return multiple-item order id
```
new_oid = order.addMultiple('C1', ['S1', 'S3'], ['I1', 'I3'], [2, 1])
```

### Remove Order and Item

#### remove a whole order

```
order.removeOrder(oid)
```

#### remove an item from an order

```
order.removeItem(oid, iid, sid)
```
# How to use Customer.py
```
customer = Customer()
```
### return all customers

```
all_customers = customer.showAll()
```

### add a new customer

```
new_cid = customer.addOne('5555', 'Tsim Sha Tsui')
```