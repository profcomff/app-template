from glob import glob
import nltk
import pickle
import json
nltk.download('popular')

token = 'Токен для связи с тг ботом'
name_qa_model = "timpal0l/mdeberta-v3-base-squad2"
name_emb_model = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
root = "bot/data_base"
replace_dict = {'посвят': 'Посвящение дня физика',
                'посвящ': 'Посвящение дня физика',
                'время': 'часы',
                'фф': 'физический факультет',
                'физфак': 'физический факультет',
                'расскажи': 'что такое',
                'какие': 'список',
                'вус': 'военно-учетный стол',
                'студсовет': 'выборный Студенческий совет 2011',
                'студенческий совет': 'выборный Студенческий совет 2011',
                'дф': 'День Физика',
                'мфк': 'Межфакультетские курсы',
                'студком':'Сдуденческий комитет',
                'скольки':'часы',
                'каким образом':'этапы',
                'быт':'студком',
                'задачи':'цели'
                }

def load_data(root: str) -> list:
    data_list = []
    for text_path in glob(f"{root}/*.txt", recursive=True):
        with open(text_path, "r") as f:
            data_list.append(f.read())
    return data_list

data_list=load_data(root)

with open('bot/data_base/dict_links.json', 'r', encoding='utf-8') as f:
    dict_links = json.loads(f.read())

with open('bot/data_base/lemmatized_profanities.pkl', 'rb') as f:
    profanities = pickle.load(f)