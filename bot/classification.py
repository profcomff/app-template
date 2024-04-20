from langchain.embeddings import HuggingFaceEmbeddings
import pandas as pd
import numpy as np
import pickle
from sklearn.neighbors import KNeighborsClassifier


def init_context_model(path_to_model):
    with open(path_to_model, 'rb') as f:
        model = pickle.load(f)
    return model


def init_bert4emb():
    model_name="cointegrated/rubert-tiny2"

    embeddings = HuggingFaceEmbeddings(
        model_name="cointegrated/rubert-tiny2",
        encode_kwargs={'normalize_embeddings': True}
        )
    return embeddings


def make_embeddings(text):
  text_emb = np.array(embeddings.embed_query(text))
  return text_emb


def get_label(text):
    text_emb = np.array([embeddings.embed_query(text)])
    label = model.predict(text_emb.reshape(1, -1))
    return label


model = init_context_model('/content/KNN_best.pkl')
embeddings = init_bert4emb()
