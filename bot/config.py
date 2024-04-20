from glob import glob

token = 'Токен для связи с тг ботом'
name_qa_model = "timpal0l/mdeberta-v3-base-squad2"
name_emb_model = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
root = "bot/data"
replace_dict = {'посвят': 'Посвящение дня физика',
                'посвящ': 'Посвящение дня физика',
                'время': 'часы',
                'фф': 'физический факультет',
                'расскажи': 'что такое',
                'какие': 'список',
                'вус': 'военно-учетный стол',
                'студсовет': 'выборный Студенческий совет 2011',
                'дф': 'День Физика',
                'мфк': 'Межфакультетские курсы',
                'студком':'Сдуденческий комитет',
                'скольки':'часы'
                }

def load_data(root: str) -> list:
    data_list = []
    for text_path in glob(f"{root}/*.txt", recursive=True):
        with open(text_path, "r") as f:
            data_list.append(f.read())
    return data_list

data_list=load_data(root)

dict_links = {
    # data_list[0]:{'Профком':'https://www.profcomff.com/'},
    # data_list[1]:{'Физфак':'https://www.phys.msu.ru/rus/about/structure/div/'},
    # data_list[2]:{'Судсовет':'https://vk.com/sovet_phys'},
    # data_list[3]:{'Часы работы':'https://vk.com/@ff_mgu-chasy-raboty-podrazdelenii-fakulteta'},
    # data_list[4]:{'ОКДФ':'https://vk.com/df_msu'},
    # data_list[5]:{'Медосмотр':'https://open.phys.msu.ru/admission/medical_exam/'},
    # data_list[6]:{'МФК':'https://lk.msu.ru/course'},
    # data_list[7]:{'Стипендиальная карта':'http://www.ffl.msu.ru/students/finance/stipendialnaya-karta.php'},
    # data_list[8]:{'Студком':'https://vk.com/studcomff'},
}
