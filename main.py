#Fast API
from fastapi import FastAPI
from pydantic import BaseModel
from std2saga import Std2saga

app = FastAPI()
saga = Std2saga()

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
