class UserInfo:
  def __init__(self, question: str, number_context: int) -> None:
    self.question = question
    self.number_context = number_context
    self.contexts = []
    self.answer = ''

  def correction_que(self, replace_dict) -> None:
    question = self.question.lower()
    for i in replace_dict.keys():
      if i in question:
        question = question.replace(i, replace_dict[i])
    self.question = question

  def search_contexts(self, data_base) -> None:
    self.contexts = data_base.similarity_search(self.question)
   
  def search_answer(self, model_pipeline) -> None:
    self.answer = model_pipeline(
        question=self.question, 
        context=self.contexts[self.number_context].page_content
        )['answer'].split(".")[0]

  def correction_answer(self, data_base, model_pipeline) -> str:
    self.correction_que(self.question)
    self.search_contexts(data_base)
    self.search_answer(model_pipeline)
    
    answer = self.answer
    if answer:
      context = self.contexts[self.number_context].page_content
      for sentence in context.split("."):
        if answer in sentence:
          sentence = sentence.replace(';', '\n')
          return f"{sentence}."
    return "Ничего не найдено..."