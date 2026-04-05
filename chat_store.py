import pymongo
from datetime import datetime, timezone
import random


class Storage:
    def __init__(self, client, db_name, collection_name, limit):
        self.db = client[db_name]
        self.messages = self.db[collection_name]
        self.summaries = self.db['summaries']
        self.limit = limit

    def save_message(self, villager_id, user_id, content):
        self.messages.insert_one({
            "villager_id": villager_id,
            "user_id": user_id,
            "content": content,
            "created_at": datetime.now(timezone.utc)
        })

        if random.random() < 0.2:
            self.trim_messages(villager_id, user_id)

    def save_summary(self, villager_id, user_id, summary):
        self.summaries.update_one(
            {"villager_id": villager_id, "user_id": user_id},
            {"$set": {"summary": summary}},
            upsert=True
        )

    def get_summary(self, villager_id, user_id):
        result = self.summaries.find_one({
            "villager_id": villager_id,
            "user_id": user_id
        })

        return result["summary"] if result else None

    def get_recent(self, villager_id, user_id, limit=10):
        chats = list(self.messages.find(
            {
                "villager_id": villager_id,
                "user_id": user_id
            }
        ).sort("created_at", -1).limit(limit))[::-1]

        return [x["content"] for x in chats]

    def trim_messages(self, villager_id, user_id):
        old_docs = list(self.messages.find(
            {
                "villager_id": villager_id,
                "user_id": user_id
            },
            {"_id": 1}
        ).sort("created_at", -1).skip(self.limit))

        if old_docs:
            ids = [doc["_id"] for doc in old_docs]

            self.messages.delete_many({
                "_id": {"$in": ids}
            })