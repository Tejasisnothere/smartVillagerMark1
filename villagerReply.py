from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from os import getenv
import json

load_dotenv()






class Replier:
    def __init__(self):
        key = getenv('GROQ_API_KEY')
        self.model = ChatGroq(model='llama-3.3-70b-versatile',api_key=key)

        self.initiatePrompt = PromptTemplate(
            template = self.loadTemplate("initiate"),
            
        )

        self.replyPrompt = PromptTemplate(
            template = self.loadTemplate("reply"),
            input_variables=['summary','chat']
        )


        self.parser = StrOutputParser()

        self.initiateChain = self.initiatePrompt | self.model | self.parser
        self.replyChain = self.replyPrompt | self.model | self.parser


    def loadTemplate(self, templateName):
        with open("templates.json", "r") as f:
            templates = json.load(f)

            return templates[f"{templateName}"]['template']
        


    def chatBuilder(self, chat):
        latest_chat = ""
        for i in chat:
            latest_chat+=i+"\n"
        

        return latest_chat
    
    def initiate(self):
        result = self.initiateChain.invoke({})
        return result
    
    def reply(self,chat, summary):
        chat = self.chatBuilder(chat)
        result = self.replyChain.invoke({"chat":chat, "summary":summary})
        return result




