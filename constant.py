import pickle

import joblib
import os.path

from fastai.basic_train import load_learner, torch

current_path = os.path.abspath(os.path.dirname(__file__))
clf = load_learner(os.path.join(current_path,'saved_models'))
# clf = joblib.load(os.path.join(current_path,'saved_models/data.pkl'))

INTENT_THRESHOLD = 94 #magical number


class TYPE_NAME_SEARCH_TTHC:
    THU_TUC = 0,
    CO_QUAN = 1,
    LINH_VUC = 2

list_chiphi_notification = ['tiền', 'phí', 'bao nhiêu', 'rẻ', 'đắt', 'giá']
list_giayto_notification = ['giấy tờ', 'cmnd', 'hồ sơ']
list_ketqua_notification = ['được gì', 'ích gì', 'kết quả']
list_thoigian_notification = ['bao lâu', 'khi nào', 'thời gian', 'chờ', 'mấy ngày', 'ngày']
list_thuchien_notification = ['bước', 'thực hiện', 'trình tự', 'làm gì', 'cách làm']
list_diadiem_notification = ['ở đâu', 'chỗ nào', 'đi đâu', 'tiếp nhận', 'địa điểm', 'địa chỉ']