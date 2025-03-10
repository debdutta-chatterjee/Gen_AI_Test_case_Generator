import os
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self,api_key,model):
        self.api_key=api_key
        self.model=model

    def get_llm_model(self):
        try:
            llm = ChatGroq(
                api_key =self.api_key, 
                model=self.model,
                streaming=True,
                temperature=0
                )
        except Exception as e:
            raise ValueError(f"Error Occurred with Exception : {e}")
        return llm