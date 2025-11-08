# my_llm.py
from langchain import LLMChain, PromptTemplate
from langchain.llms.base import LLM

class MyLLM(LLM):
    def _call(self, prompt: str, stop=None):
        # custom inference logic to your hosted LLM API
        return f"LLM response for: {prompt}"

    @property
    def _identifying_params(self):
        return {"name": "MyLLM"}

    @property
    def _llm_type(self):
        return "custom_llm"

template = "You are an AI. Answer clearly: {question}"
prompt = PromptTemplate.from_template(template)
chain = LLMChain(llm=MyLLM(), prompt=prompt)

