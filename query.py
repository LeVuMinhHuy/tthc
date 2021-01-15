from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sal
from sqlalchemy.sql import text
from elasticsearch import Elasticsearch

from constant import TYPE_NAME_SEARCH_TTHC, TENTTHC_THRESHOLD_SCORE

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
engine = sal.create_engine(
    "mssql+pyodbc://SA:I@maman99@localhost/TTHC?driver=ODBC+Driver+17+for+SQL+Server")
con = engine.connect()

Base = declarative_base()

def search(case, query):
    if case == TYPE_NAME_SEARCH_TTHC.THU_TUC:
        result = searchTTHC(query)
        filter_result = list(filter(lambda x: x['_score'] > TENTTHC_THRESHOLD_SCORE, result))
        IDs = tuple(map(lambda x: x['_id'], filter_result))
        return queryExactTTHC(IDs).fetchall()
    elif case == TYPE_NAME_SEARCH_TTHC.CO_QUAN:
        mostMatch = searchCoQuan(query, 1)
        return queryCoQuan(mostMatch[0]['_id']).fetchall()
    elif case == TYPE_NAME_SEARCH_TTHC.LINH_VUC:
        mostMatch = searchLinhVuc(query, 1)
        return queryLinhVuc(mostMatch[0]['_id']).fetchall()
    return []


def searchTTHC(query):
    result = es.search(index="tentthc", body={"query": {
        "query_string": {
            "query": query,
        }}})
    return result['hits']['hits']


def searchCoQuan(query, limit):
    result = es.search(index="coquan", body={"query": {
        "query_string": {
            "query": query,
        }}})
    return result['hits']['hits'][:limit]


def searchLinhVuc(query, limit):
    result = es.search(index="linhvuc", body={"query": {
        "query_string": {
            "query": query,
        }}})
    return result['hits']['hits'][:limit]


def queryExactTTHC(IDs):
    rows = con.execute(
        text("SELECT * FROM ThuTucChiTiet WHERE ID IN {}".format(IDs)))
    if rows:
        return rows
    else:
        return None


def queryLinhVuc(MaLinhVuc):
    rows = con.execute(
        text("SELECT ThuTucChiTiet.* FROM  ThuTucChiTiet JOIN ThuTucChiTietLinhVucThucHien ON ThuTucChiTiet.MaTTHC=ThuTucChiTietLinhVucThucHien.MaTTHC WHERE MaLinhVuc=N'{}'".format(MaLinhVuc)))
    if rows:
        return rows
    else:
        return []


def queryCoQuan(MaDonVi):
    rows = con.execute(
        text("SELECT ThuTucChiTiet.* FROM  ThuTucChiTiet JOIN ThuTucChiTietCoQuanThucHien ON ThuTucChiTiet.MaTTHC=ThuTucChiTietCoQuanThucHien.MaTTHC WHERE MaDonVi=N'{}'".format(MaDonVi)))
    if rows:
        return rows
    else:
        return []
