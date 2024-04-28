from mysql import connector
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection


# class DB(MySQLConnectionAbstract):
class DB:

    def __init__(self):
        # super.__init__()
        try:
            self.db = connector.connect(
            # self = connector.connect(
                host="localhost",
                user="localBoy",
                password="sipsipigaveyoufullsip",
                database="tmd_water_db"
            )
            self.test_connection()
        except:
            print("can not acces to database!")
            exit(0)
    
    def test_connection(self):
        # self.db.cursor().execute("select * from District;")
        cs = self.db.cursor()
        cs.execute("select * from District;")
        # print
        for x in cs.fetchall():
            print(x)
