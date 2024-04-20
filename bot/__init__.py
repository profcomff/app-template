from .init_model import data_base, model_pipeline
from .UserInfo import UserInfo
from .config import replace_dict

sessions = {}

def answer(question: str, uid: int):
    return UserInfo(question, 0).correction_answer(data_base, model_pipeline, replace_dict)