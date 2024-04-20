import torch
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from transformers import pipeline, AutoTokenizer
from optimum.onnxruntime import ORTModelForQuestionAnswering

from config import name_emb_model, name_qa_model, data_list

def init_qa_model(name_qa_model: str):
    model = ORTModelForQuestionAnswering.from_pretrained(name_qa_model, from_transformers=True)
    tokenizer = AutoTokenizer.from_pretrained(name_qa_model)
    tokenizer.model_input_names = ['input_ids', 'attention_mask']

    model_pipeline = pipeline(
        task='question-answering',
        model=model,
        tokenizer=tokenizer,
        device= torch.device("cuda" if torch.cuda.is_available() else "cpu")
        )
    
    return model_pipeline

def init_emb_model(name_emb_model: str, data_list: list):
    embeddings = HuggingFaceEmbeddings(
        model_name=name_emb_model, 
        encode_kwargs={'normalize_embeddings': True}
        )
    
    data_base = FAISS.from_texts(data_list, embeddings)
    return data_base

data_base = init_emb_model(name_emb_model, data_list)
model_pipeline = init_qa_model(name_qa_model)