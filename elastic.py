import sqlalchemy as sal
from elasticsearch import Elasticsearch
from sqlalchemy.sql import text

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
engine = sal.create_engine(
    "mssql+pyodbc://SA:I@maman99@localhost/TTHC?driver=ODBC+Driver+17+for+SQL+Server")

con = engine.connect()

rows = con.execute(
    text("SELECT ID,TenTTHC FROM ThuTucChiTiet"))
counter = 0
for r in rows:
    if counter == 1796:
        counter = counter+1
        continue
    es.create(index="tentthc", id=r[0], body={"name": r[1]})
    counter = counter+1


rows = con.execute(
    text("SELECT TenLinhVuc,MaLinhVuc,COUNT(ID) FROM ThuTucChiTietLinhVucThucHien GROUP BY TenLinhVuc,MaLinhVuc"))
counter = 0
for r in rows:
    es.create(index="linhvuc", id=r[1], body={"name": r[0], "id": r[1], "count": r[2]})
    counter = counter + 1

rows = con.execute(
    text("SELECT TenDonVi,MaDonVi,COUNT(ID) FROM ThuTucChiTietCoQuanThucHien GROUP BY TenDonVi,MaDonVi"))
counter = 0
for r in rows:
    es.create(index="coquan", id=r[1], body={"name": r[0], "id": r[1], "count": r[2]})
    counter = counter + 1
