from fastapi import FastAPI, Request
import pymongo
import os
from dotenv import load_dotenv
from chat_store import Storage
from chain import Chain
import threading

load_dotenv()
app = FastAPI()


aiReplier = Chain()


@app.post('/right_click')
async def right_click_event(request: Request):
    data = await request.json()
    print("right click:", data)

    villager_id = data.get("villagerID")
    user_id = data.get("userID")

    
    reply = aiReplier.getReply(vid=villager_id, uid=user_id, userMessage="")
    
    # threading.Thread(
    #     target=backgroundSave,
    #     args=villager_id
    # ).start()
    backgroundSave(villager_id)
    

    print(reply)

    return {"message": reply}


@app.post('/message')
async def message(request: Request):
    data = await request.json()
    user_id = data.get('userID')
    user_message = data.get('userMessage')
    print("message:", data)

    villager_id = None
    with open("latestID.txt", 'r') as f:
        villager_id=f.read()

    reply = aiReplier.getReply(vid=villager_id, uid=user_id, userMessage="user"+user_message)
    
    print(reply)
    return {"message": reply}


@app.post('/event/left_click')
async def left_click_event():
    return {"message": "Left click received"}


def backgroundSave(villager_id):
    with open("latestID.txt", 'w') as f:
        f.write(villager_id)