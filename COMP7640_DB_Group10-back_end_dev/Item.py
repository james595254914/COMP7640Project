from db import connection


class Item:

    def __init__(self):
        self.conn = connection()

    def listAllItemByShop(self, sid) -> tuple:
        """
        return all items of one shop
        @sid: shop id
        """
        cursor = self.conn.cursor()
        cursor.execute('select * from Item where sid="{}"'.format(sid))
        items = cursor.fetchall()
        cursor.close
        return items

    def addOne(self, iname, price, item_qty, sid, kw1, kw2='', kw3=''):
        """
        add one item for one shop and return the id of the new item
        @iname: item name
        @price: item price
        @item_qty: item quantity
        @sid: shop id
        @kw1: keyword
        @kw2: keyword
        @kw3: keyword
        """
        cursor = self.conn.cursor()
        cursor.execute('select iid from Item where sid="{}"'.format(sid))
        iids = [int(i[0][1:]) for i in cursor.fetchall()]
        if len(iids) == 0:
            new_iid = 'I1'
        else:
            new_iid = 'I' + str(max(iids) + 1)
        sql = 'insert into Item values ("{}", "{}", "{}", {}, "{}","{}","{}", {})'.format(
            new_iid, sid, iname, price, kw1, kw2, kw3, item_qty)
        try:
            cursor.execute(sql)
            self.conn.commit()
        except Exception:
            return False
        cursor.execute('select iid from Item where iid="{}" and sid="{}"'.format(new_iid, sid))
        iid_in_mysql = cursor.fetchall()[0][0]
        cursor.close()
        return iid_in_mysql

    def search(self, key) -> tuple:
        """
        item search
        @key: the name or the keyword of the item(s)
        """
        cursor = self.conn.cursor()
        key = key.lower()
        sql = 'select iid, iname, price, item_qty, sid from Item where LOWER(iname)="{}" or LOWER(kw1)="{}" or LOWER(kw2)="{}" or LOWER(kw3)="{}"'.format(
            key, key, key, key)
        cursor.execute(sql)
        items = cursor.fetchall()
        cursor.close()
        return items

    def __del__(self):
        self.conn.close()