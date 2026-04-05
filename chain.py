from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from chat_store import Storage
from summarize import Summarizer
from villagerReply import Replier
import os
import threading
import pymongo

load_dotenv()

mongo_client = os.getenv('MONGO_URL')
client = pymongo.MongoClient(mongo_client)

db_name = "MinecraftDB1"
collection_name = "villager"





class Chain:
    def __init__(self):
        self.store = Storage(client=client, database=db_name, collection_name=collection_name, limit=5)
        self.replier = Replier()
        self.summObj = Summarizer()


        
    def extendConvo(self,chat,summary):
        return self.replier.reply(chat,summary)

    def InitiateConvo(self):
        return self.replier.initiate()
    
    def saveSummary(self):
        return self.summObj.summarizeChat(self.chat)
    
    def getReply(self, vid, uid, userMessage):
        
        if not vid or not uid:
            return "Null uid or vid"


        if userMessage:
            self.store.save_message(vid,uid,userMessage)

        chat = self.store.getrecent(vid,uid)
        reply = None

        if(len(chat)==0):
            reply = self.InitiateConvo()

        else:
            summary = self.store.get_summary(vid,uid)
            reply = self.extendConvo(chat,summary)
            

        threading.Thread(
            target=self.background_worker,
            args = (vid,uid,reply)
        ).start()
        
        
        return reply
    
    def background_worker(self, vid, uid, reply):
        try:
            self.store.save_message(vid,uid,reply)
            chat = self.store.getrecent(vid,uid)
            self.summary = self.summObj.summarizeChat(chat)
            self.store.save_summary(vid,uid,self.summary)
        except Exception as e:
            print("Background error", e)


