from db import connection


class Shop:

    def __init__(self):
        self.conn = connection()

    def showAll(self) -> tuple:
        """
        return all shops
        """
        cursor = self.conn.cursor()
        cursor.execute('select * from Shop')
        shops = cursor.fetchall()
        cursor.close()
        return shops

    def addOne(self, sname, rating, address):
        """
        add one shop and return the id of the new shop
        @sname: shop name
        @rating: shop rating
        @address: shop address
        """
        cursor = self.conn.cursor()
        cursor.execute('select sid from Shop')
        sids = [int(s[0][1:]) for s in cursor.fetchall()]
        new_sid = 'S' + str(max(sids) + 1)
        sql = 'insert into Shop values ("{}", "{}", {}, "{}")'.format(
            new_sid, sname, rating, address)
        try:
            cursor.execute(sql)
            self.conn.commit()
        except Exception:
            return False
        cursor.execute('select sid from Shop where sid="{}"'.format(new_sid))
        sid_in_mysql = cursor.fetchall()[0][0]
        cursor.close()
        return sid_in_mysql

    def __del__(self):
        self.conn.close()