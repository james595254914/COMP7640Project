import sys
from db import connection


class Order(object):

    def __init__(self):
        self.conn = connection()

    def getOrdersByUser(self, cid) -> tuple:
        '''
        Get Orders by User id
        @cid: customer id

        return: a `tuple` contain all orders of user `uid`
            key order: `oid` 
        '''
        cursor = self.conn.cursor()
        cursor.execute('select oid from Order_info where cid="{}";'.format(cid))
        oid_set = cursor.fetchall()
        cursor.close()
        return oid_set

    def getItemsByOrder(self, oid, cid=None) -> tuple:
        '''
        Get Items by order id
        @oid: order id

        return: a `tuple` contain all item information for all item found by `oid`
            key order: `iid`, `sid`, `iname`, `price`, `kw1`, `kw2`, `kw3`, `Item_qty`
        '''
        cursor = self.conn.cursor()
        cursor.execute('select I.iid, I.sid, I.iname, I.price, I.kw1, I.kw2, I.kw3, I.Item_qty from Item as I RIGHT JOIN Orders as O on (I.iid=O.iid and I.sid=O.sid) where oid="{}";'.format(oid))
        item_list = cursor.fetchall()
        cursor.close()
        return item_list

    def getOrders(self, cid=None, oid=None, **kwargs) -> tuple:
        '''
        Get Orders according to the query. 
        @cid: Customer ID
        @oid: Order ID
        @**kwargs: any legal search query, use at your own risk 

        return: a `tuple` contain all found entries represented by `tuple` for each entry. 
            key order: `oid`, `cid`, `sid`, `iid`, `price`, `Order_qty`, `total`
        '''
        # 实际上就是把 SQL 的 SELECT 打包了一下 （笑
        cursor = self.conn.cursor()

        # Parse search query.
        if cid != None:
            kwargs['cid'] = cid
        if oid != None:
            kwargs['Order_info.oid'] = oid
        condition_query = ''
        for key, value in kwargs.items():
            if len(condition_query.strip()) < 1:
                condition_query += ' WHERE '
            else:
                condition_query += ' AND '
            condition_query += '{}="{}"'.format(key, value)

        cursor.execute('select Order_info.oid, cid, sid, iid, price, Order_qty, total from Orders LEFT JOIN Order_info ON Orders.oid=Order_info.oid {};'.format(condition_query))
        orders = cursor.fetchall()
        cursor.close()
        return orders

    def itemQuantity(self, sid, iid) -> int:
        """
        return the quantity of one item in its shop
        @sid: shop id
        @iid: item id
        """
        cursor = self.conn.cursor()
        cursor.execute(
            'select item_qty from Item where sid="{}" and iid="{}"'.format(
                sid, iid))
        item_qty = cursor.fetchall()[0][0]
        cursor.close()
        return item_qty

    def addOne(self, cid, sid, iid, order_qty):
        """
        add one item purchase and return the id of the whole order
        @cid: customer id
        @sid: shop id
        @iid: item id
        @order_qty: order quantity of the item
        """
        cursor = self.conn.cursor()
        cursor.execute(
            'select price, item_qty from Item where sid="{}" and iid="{}"'.
            format(sid, iid))
        price, item_qty = cursor.fetchall()[0]
        if order_qty > item_qty:
            return False
            sys.exit(1)
        cursor.execute('select oid from Orders')
        oids = [int(o[0][1:]) for o in cursor.fetchall()]
        if len(oids) == 0:
            new_oid = 'O1'
        else:
            new_oid = 'O' + str(max(oids) + 1)
        try:
            cursor.execute('insert into Order_info values ("{}", "{}")'.format(new_oid, cid))
            self.conn.commit()
        except Exception:
            return False
        sql = 'insert into Orders values ("{}", "{}", "{}", {}, {}, {})'.format(
            new_oid, sid, iid, price, order_qty, price * order_qty)
        try:
            cursor.execute(sql)
            self.conn.commit()
        except Exception:
            return False
        cursor.execute('select oid from Orders where oid="{}"'.format(new_oid))
        oid_in_mysql = cursor.fetchall()[0][0]
        cursor.close()
        return oid_in_mysql

    def addMultiple(self, cid, sid_l, iid_l, order_qty_l):
        """
        add multiple items purchase and return the id of the whole order
        @cid: customer id
        @sid_l: shop ids list
        @iid_l: item ids list
        @order_qty_l: order quantities list of each item
        """
        cursor = self.conn.cursor()
        cursor.execute('select oid from Orders')
        oids = [int(o[0][1:]) for o in cursor.fetchall()]
        if len(oids) == 0:
            new_oid = 'O1'
        else:
            new_oid = 'O' + str(max(oids) + 1)
        try:
            cursor.execute('insert into Order_info values ("{}", "{}")'.format(new_oid, cid))
            self.conn.commit()
        except Exception:
            return False
        mul_sql = 'insert into Orders values'
        for sid, iid, order_qty in zip(sid_l, iid_l, order_qty_l):
            cursor.execute(
                'select price, item_qty from Item where sid="{}" and iid="{}"'.
                format(sid, iid))
            price, item_qty = cursor.fetchall()[0]
            if order_qty > item_qty:
                return False
                sys.exit(1)
            mul_sql += ' ("{}", "{}", "{}", {}, {}, {}),'.format(
                new_oid, sid, iid, price, order_qty, price * order_qty)
        try:
            cursor.execute(mul_sql[:-1])
            self.conn.commit()
        except Exception:
            return False
        cursor.execute(
            'select distinct(oid) from Orders where oid="{}"'.format(new_oid))
        oid_in_mysql = cursor.fetchall()[0][0]
        cursor.close()
        return oid_in_mysql

    def removeOrder(self, oid) -> bool:
        '''
        Cancel a whole order. 
        @oid: order id to cancel. 
        '''
        cursor = self.conn.cursor()
        try:
            cursor.execute('DELETE FROM Orders WHERE oid="{}";'.format(oid))
        except:
            return False

        self.conn.commit()
        cursor.close()
        return True

    def removeItem(self, oid, iid, sid) -> bool:
        '''
        Remove an item from an order. 
        @oid: order id
        @iid: item id
        @sid: shop id
        '''
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                'DELETE FROM Orders WHERE oid="{}" AND iid="{}" AND sid="{}";'.
                format(oid, iid, sid))
        except:
            return False

        self.conn.commit()
        cursor.close()
        return True

    def __del__(self):
        self.conn.close()
