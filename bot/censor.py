from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from string import punctuation
from numpy import array, any
from pymorphy3 import MorphAnalyzer

<<<<<<< Updated upstream
def hui(
    text:str, 
=======
def censor(
    question:str, 
>>>>>>> Stashed changes
    profanities: list
    ) -> bool:
  question = question.lower().translate(str.maketrans('', '', punctuation))

  tokens = word_tokenize(question)
  filtered_tokens = array(tokens)

  morph = MorphAnalyzer()
  lemmatization = lambda w: morph.parse(w)[0].normal_form
  bad_words_in_text_mask = [lemmatization(word) in profanities for word in filtered_tokens]

  check = any(bad_words_in_text_mask)
  return check

def filter_question(question, filter_emb, filter_ml) -> int:
  question_emb = array([filter_emb.embed_query(question)])
  label = filter_ml.predict(question_emb.reshape(1, -1))
  return label