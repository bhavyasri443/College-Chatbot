from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

# Serve frontend
@app.get("/")
def home():
    return FileResponse("index.html")

class Message(BaseModel):
    message: str

@app.post("/chat")
def chat(msg: Message):
    text = msg.message.lower()

    if "hi" in text or "hello" in text:
        return {"reply": "Hello 👋 Welcome to MRECW!"}

    if "highest package" in text:
        return {"reply": "The highest package is ₹32 LPA by Visa."}

    if "placements" in text:
        return {"reply": "1100+ placements. Top recruiters: Amazon, Infosys, Deloitte."}

    return {"reply": "Please ask about placements or highest package."}
