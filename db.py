import fdb


class DataBase:
    def __init__(self):
        self.con = fdb.connect(dsn='asup5:D:Master\Data\BUHDATA.GDB', user='sysdba',
                          password='masterkey')

        self.cur = self.con.cursor()

singleton_db = DataBase().cur