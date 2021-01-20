import pickle

import joblib
import os.path

from fastai.text import *

current_path = os.path.abspath(os.path.dirname(__file__))
clf = load_learner(os.path.join(current_path, 'saved_models'))

INTENT_THRESHOLD = 94  # magical number
TENTTHC_THRESHOLD_SCORE = 7 # ???

class TYPE_NAME_SEARCH_TTHC:
    THU_TUC = 0,
    CO_QUAN = 1,
    LINH_VUC = 2


list_chiphi_notification = ['tiền', 'phí', 'bao nhiêu', 'rẻ', 'đắt', 'giá']
list_giayto_notification = ['giấy tờ', 'hồ sơ', 'cmnd', 'chứng minh nhân dân', 'bản chính', 'bản sao', 'bản gốc', 'biên bản']
list_ketqua_notification = ['được gì', 'ích gì', 'kết quả']
list_thoigian_notification = [
    'bao lâu', 'khi nào', 'thời gian', 'chờ', 'mấy ngày', 'ngày']
list_thuchien_notification = [
    'bước', 'thực hiện', 'trình tự', 'làm gì', 'cách làm', 'quy trình']
list_diadiem_notification = ['ở đâu', 'chỗ nào',
                             'đi đâu', 'tiếp nhận', 'địa điểm', 'địa chỉ']


class INTENT_TYPE:
    CHI_PHI = 'chiphi'
    DIA_DIEM = 'diadiem'
    GIAY_TO = 'giayto'
    KET_QUA = 'ketqua'
    THOI_GIAN = 'thoigian'
    THUC_HIEN = 'thuchien'