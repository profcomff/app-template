from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from string import punctuation
from numpy import array, any
from pymorphy3 import MorphAnalyzer

def hui(
    text:str, 
    profanities: list
    ) -> bool:
  text = text.lower().translate(str.maketrans('', '', punctuation))

  tokens = word_tokenize(text)
  filtered_tokens = array(tokens)

  morph = MorphAnalyzer()
  amogus = lambda w: morph.parse(w)[0].normal_form
  bad_words_in_text_mask = [amogus(word) in profanities for word in filtered_tokens]

  check = any(bad_words_in_text_mask)
  return check
