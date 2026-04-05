import pymongo
from datetime import datetime, timezone
import random

client = pymongo.MongoClient("mongodb://localhost:27017/")


class Storage():
    def __init__(self, client, db_name, collection_name, limit):
        self.db = client[db_name]
        self.messages = self.db[collection_name]
        self.summaries = self.db['summaries']
        self.limit = limit
        

def save_message(self, villager_id, user_id, content, limit=50):
    self.messages.insert_one({
        "villager_id":villager_id,
        "user_id":user_id,
        "content": content,
        "created_at":datetime.now(timezone.utc)
    })

    if random.random() < 0.2:
        self.trim_messages(villager_id, user_id, limit)



def save_summary(self, villager_id, user_id, summary):

    my_query = {'villager_id':villager_id, 'user_id':user_id}
    self.summaries.delete_one(my_query)

    self.summaries.insert_one({
        "villager_id":villager_id,
        "user_id":user_id,
        "summary":summary
    })

def get_summary(self, villager_id, user_id):
    my_query = {'villager_id':villager_id, 'user_id':user_id}
    result = self.summaries.find(my_query)
    return result['summary']


def get_recent(self, villager_id, user_id, limit=10):
    chats = list(self.messages.find(
        {
            "villager_id": villager_id,
            "user_id": user_id
        }
    ).sort("created_at", -1).limit(limit))[::-1]

    chats = [x['content'] for x in chats]
    return chats




def trim_messages(self, villager_id, user_id, limit=50):
    self.messages.delete_many({
        "_id": {
            "$in": self.messages.find(
                {
                    "villager_id": villager_id,
                    "user_id": user_id
                },
                {"_id": 1}
            ).sort("created_at", -1).skip(limit)
        }
    })