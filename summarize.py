import json
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from os import getenv


load_dotenv()


class Summarizer():

    def __init__(self):
        key = getenv('GROQ_API_KEY')
        self.model = ChatGroq(model='llama-3.3-70b-versatile',api_key=key)

        self.prompt = PromptTemplate(
            template=self.loadTemplate('summarize'),
            input_variables=['chat']
        )

        self.parser = StrOutputParser()

        self.chain = self.prompt | self.model | self.parser


    def loadTemplate(self, templateName):
        with open("templates.json", "r") as f:
            templates = json.load(f)

            return templates[f"{templateName}"]['template']

    def summarizeChat(self, chat):
        
        result = self.chain.invoke({"chat":chat})
        return result
