from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sal
from sqlalchemy.sql import text
from elasticsearch import Elasticsearch

from constant import TYPE_NAME_SEARCH_TTHC, TENTTHC_THRESHOLD_SCORE, INTENT_TYPE

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
engine = sal.create_engine(
    "mssql+pyodbc://SA:I@maman99@localhost/TTHC?driver=ODBC+Driver+17+for+SQL+Server")
con = engine.connect()

Base = declarative_base()

def search(case, query):
    if case == TYPE_NAME_SEARCH_TTHC.THU_TUC:
        result = searchTTHC(query)
        filter_result = list(filter(lambda x: x['_score'] > TENTTHC_THRESHOLD_SCORE, result))
        if (len(filter_result) == 0):
            return [[],{'type': 'unknown', 'count': 0}]
        IDs = tuple(map(lambda x: x['_id'], filter_result))
        if (len(IDs) == 0):
            return [[],{'type': 'unknown', 'count': 0}]
        TTHC = queryExactTTHC(IDs).fetchall()
        return [TTHC, {'type': 'tentthc', 'count': len(TTHC)}]

    elif case == TYPE_NAME_SEARCH_TTHC.CO_QUAN:
        mostMatch = searchCoQuan(query, 1)
        filter_mostMatch = list(filter(lambda x: x['_score'] > TENTTHC_THRESHOLD_SCORE, mostMatch))
        if (len(filter_mostMatch) == 0):
            return [[],{'type': 'unknown', 'count': 0}]
        IDs = tuple(map(lambda x: x[0], queryCoQuan(filter_mostMatch[0]['_id']).fetchall()))
        if (len(IDs) == 0):
            return [[],{'type': 'unknown', 'count': 0}]
        
        TTHC = queryCoQuan(mostMatch[0]['_id']).fetchall()
        if (len(TTHC) < 4):
            return [TTHC, {'type': 'coquan', 'count': len(TTHC)}]

        linhvuc = queryLinhVucByMaTTHC(IDs).fetchall()
        return [linhvuc, {'type': 'coquan_linhvuc', 'count': len(TTHC)}]

    elif case == TYPE_NAME_SEARCH_TTHC.LINH_VUC:
        mostMatch = searchLinhVuc(query, 1)
        filter_mostMatch = list(filter(lambda x: x['_score'] > TENTTHC_THRESHOLD_SCORE, mostMatch))
        if (len(filter_mostMatch) == 0):
            return [[],{'type': 'unknown', 'count': 0}]
        TTHC = queryLinhVuc(filter_mostMatch[0]['_id']).fetchall()
        return [TTHC, {'type': 'linhvuc', 'count': len(TTHC)}]

    return [[],{'type': 'unknown', 'count': 0}]


def get_info(intent, maTTHC):
    if (intent == INTENT_TYPE.DIA_DIEM):
        result = queryDiadiem(maTTHC).fetchall()
        return [result, {'type': 'diadiem', 'count': len(result)}]
    if (intent == INTENT_TYPE.CHI_PHI):
        result = queryChiphi(maTTHC).fetchall()
        return [result, {'type': 'chiphi', 'count': len(result)}]
    if (intent == INTENT_TYPE.GIAY_TO):
        result = queryGiayto(maTTHC).fetchall()
        return [result, {'type': 'giayto', 'count': len(result)}]
    if (intent == INTENT_TYPE.KET_QUA):
        result = queryKetqua(maTTHC).fetchall()
        return [result, {'type': 'ketqua', 'count': len(result)}]
    if (intent == INTENT_TYPE.THOI_GIAN):
        result = queryThoigian(maTTHC).fetchall()
        return [result, {'type': 'thoigian', 'count': len(result)}]
    if (intent == INTENT_TYPE.THUC_HIEN):
        result = queryThuchien(maTTHC).fetchall()
        return [result, {'type': 'thuchien', 'count': len(result)}]
    return [[],{'type': 'unknown', 'count': 0}]

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
        text("SELECT T.MaTTHC, T.TenTTHC, T.DiaChiTiepNhan FROM  ThuTucChiTiet AS T WHERE ID IN ({})".format(', '.join(IDs))))
    if rows:
        return rows
    else:
        return []


def queryLinhVuc(MaLinhVuc):
    rows = con.execute(
        text("SELECT T.MaTTHC, T.TenTTHC, T.DiaChiTiepNhan FROM  ThuTucChiTiet AS T JOIN ThuTucChiTietLinhVucThucHien ON T.MaTTHC=ThuTucChiTietLinhVucThucHien.MaTTHC WHERE MaLinhVuc=N'{}'".format(MaLinhVuc)))
    if rows:
        return rows
    else:
        return []


def queryCoQuan(MaDonVi):
    rows = con.execute(
        text("SELECT T.MaTTHC, T.TenTTHC, T.DiaChiTiepNhan FROM  ThuTucChiTiet AS T JOIN ThuTucChiTietCoQuanThucHien ON T.MaTTHC=ThuTucChiTietCoQuanThucHien.MaTTHC WHERE MaDonVi=N'{}'".format(MaDonVi)))
    if rows:
        return rows
    else:
        return []

def queryLinhVucByMaTTHC(IDs):
    rows = con.execute(
        text("SELECT L.TenLinhVuc FROM ThuTucChiTietLinhVucThucHien AS L WHERE MaTTHC IN {} GROUP BY L.TenLinhVuc".format(IDs))
    )
    if rows:
        return rows
    else:
        return []

def queryDiadiem(maTTHC):
    rows = con.execute(
        text("SELECT T.DiaChiTiepNhan FROM ThuTucChiTiet AS T WHERE MaTTHC = N'{}'".format(maTTHC))
    )
    if rows:
        return rows
    else: 
        return []

def queryChiphi(maTTHC):
    rows = con.execute(
        text("SELECT P.SoTien, P.MoTa FROM (SELECT TG.Id, TG.MoTa FROM  ThoiGian AS TG JOIN (SELECT TH.Id FROM ThuTucChiTiet AS T LEFT JOIN ThuTucChiTietCachThucThucHien TH ON T.MaTTHC = TH.MaTTHC WHERE T.MaTTHC = N'{}') T ON T.Id = TG.CachThucThucHienId) AS TEMP JOIN PhiLePhi P ON TEMP.Id = P.ThoiGianId".format(maTTHC))
    )
    if rows:
        return rows
    else: 
        return []

def queryGiayto(maTTHC):
    rows = con.execute(
        text("SELECT TenGiayTo, SoBanChinh, SoBanSao, TenMauDon, Url FROM GiayTo JOIN (SELECT HS.Id FROM ThuTucChiTietThanhPhanHoSo AS HS JOIN ThuTucChiTiet T ON HS.MaTTHC = T.MaTTHC WHERE T.MaTTHC = N'{}') AS TEMP ON GiayTo.ThanhPhanHoSoId = TEMP.Id".format(maTTHC))
    )
    if rows:
        return rows
    else: 
        return []

def queryThoigian(maTTHC):
    rows = con.execute(
        text("SELECT TG.ThoiGianGiaiQuyet, TG.DonViTinh, TG.MoTa FROM  ThoiGian AS TG JOIN (SELECT TH.Id FROM ThuTucChiTiet AS T LEFT JOIN ThuTucChiTietCachThucThucHien TH ON T.MaTTHC = TH.MaTTHC WHERE T.MaTTHC = N'{}') T ON T.Id = TG.CachThucThucHienId".format(maTTHC))
    )
    if rows:
        return rows
    else: 
        return []

def queryKetqua(maTTHC):
    rows = con.execute(
        text("SELECT KQ.TenKetQua FROM ThuTucChiTietKetQuaThucHien AS KQ JOIN ThuTucChiTiet T ON KQ.MaTTHC = T.MaTTHC WHERE T.MaTTHC = N'{}'".format(maTTHC))
    )
    if rows:
        return rows
    else: 
        return []

def queryThuchien(maTTHC):
    rows = con.execute(
        text("SELECT TenTrinhTu FROM (TrinhTu AS TT JOIN (SELECT CCTT.Id FROM ThuTucChiTietTrinhTuThucHien AS CCTT JOIN ThuTucChiTiet T on T.MaTTHC = CCTT.MaTTHC WHERE T.MaTTHC = N'{}') AS TEMP ON  TEMP.Id = TT.TrinhTuThucHienId ) ORDER BY TT.Id".format(maTTHC))
    )
    if rows:
        return rows
    else: 
        return []

