from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sal
from sqlalchemy.sql import text
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
engine = sal.create_engine(
    "mssql+pyodbc://SA:Tthc2@2!@localhost/TTHC?driver=ODBC+Driver+17+for+SQL+Server")
con = engine.connect()

Base = declarative_base()

def search(case, query, limit):
    if case == 0:
        return searchTTHC(query, limit)
    elif case == 1:
        return searchCoQuan(query, limit)
    elif case == 2:
        return searchLinhVuc(query, limit)
    return []


def searchTTHC(query, limit=5):
    result = es.search(index="tentthc3", body={"query": {
        "query_string": {
            "query": query,
        }}})
    return result['hits']['hits'][:limit]


def searchCoQuan(query, limit=3):
    result = es.search(index="coquan", body={"query": {
        "query_string": {
            "query": query,
        }}})
    return result['hits']['hits'][:limit]


def searchLinhVuc(query, limit=3):
    result = es.search(index="linhvuc", body={"query": {
        "query_string": {
            "query": query,
        }}})
    return result['hits']['hits'][:limit]


def query(case, ID):
    if case == 0:
        return queryExactTTHC(ID)
    elif case == 1:
        return queryLinhVuc(ID)
    elif case == 2:
        return queryCoQuan(ID)
    return []


def queryExactTTHC(ID):
    rows = con.execute(
        text("SELECT * FROM ThuTucChiTiet WHERE ID={}".format(ID)))
    if rows:
        return rows[0]
    else:
        return None


def queryLinhVuc(MaLinhVuc):
    rows = con.execute(
        text("SELECT ThuTucChiTiet.* FROM  ThuTucChiTiet JOIN ThuTucChiTietLinhVucThucHien ON ThuTucChiTiet.MaTTHC=ThuTucChiTietLinhVucThucHien.MaTTHC WHERE MaLinhVuc=N'{}'".format(MaLinhVuc)))
    if rows:
        return rows
    else:
        return []


def queryCoQuan(MaCoQuan):
    rows = con.execute(
        text("SELECT ThuTucChiTiet.* FROM  ThuTucChiTiet JOIN ThuTucChiTietCoQuanThucHien ON ThuTucChiTiet.MaTTHC=ThuTucChiTietCoQuanThucHien.MaTTHC WHERE MaLinhVuc=N'{}'".format(MaCoQuan)))
    if rows:
        return rows
    else:
        return []
