from db import connection


class Customer:

    def __init__(self):
        self.conn = connection()

    def showAll(self) -> tuple:
        """
        return all customers
        """
        cursor = self.conn.cursor()
        cursor.execute('select * from Customer')
        cids = cursor.fetchall()
        cursor.close()
        return cids

    def addOne(self, tel, addr):
        """
        add one customer and return the id of the new customer
        """
        cursor = self.conn.cursor()
        cursor.execute('select cid from Customer')
        cids = [int(c[0][1:]) for c in cursor.fetchall()]
        new_cid = 'C' + str(max(cids) + 1)
        sql = 'insert into Customer values ("{}", "{}", "{}")'.format(
            new_cid, tel, addr)
        try:
            cursor.execute(sql)
            self.conn.commit()
        except Exception:
            return False
        cursor.execute('select cid from Customer where cid="{}"'.format(new_cid))
        cid_in_mysql = cursor.fetchall()[0][0]
        cursor.close()
        return cid_in_mysql

    def __del__(self):
        self.conn.close()