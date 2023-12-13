#Fast API
from fastapi import FastAPI
from pydantic import BaseModel
from std2saga import Std2saga
from add_darkrai import Darkrai

app = FastAPI()
saga = Std2saga()
darkrai = Darkrai()

class Message(BaseModel):
    message: str

@app.post("/sagaben")
async def sagaben(message: Message):
    user_message = message.message
    response = saga.sagaben(str(user_message))
    return {
        "messages": [
            {"sender": "user", "text": user_message}, 
            {"sender": "bot", "text": response}
        ]
    }

@app.post("/darkrai")
async def darkrai(message: Message):
    user_message = message.message
    response = darkrai.darkrai_sentence(str(user_message))
    return {
        "messages": [
            # {"sender": "user", "text": user_message}, 
            {"sender": "bot-darkrai", "text": response}
        ]
    }