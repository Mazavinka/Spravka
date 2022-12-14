import fdb

con = fdb.connect(dsn='asup5:D:Master\Data\BUHDATA.GDB', user='sysdba',
                  password='masterkey')

cur = con.cursor()

#cur.execute("SELECT SUM(R.SUMMA) FROM UV_REZNACH R, NACHISL N WHERE KPODR=91 AND r.ndate='01.09.2022' AND TN=24039 AND R.NCODE=N.NCODE and N.PENCODE<>205")
#cur.execute("EXECUTE PROCEDURE GETNALREZ('259', '01.10.2022', '24110', '1', '0')")
cur.execute("EXECUTE PROCEDURE GETPOSREZ(3,'01.11.2022',15921, 2)")

data = cur.fetchall()
print(data)
