from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import os

app = FastAPI()

class Message(BaseModel):
    message: str

# Load JSON file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(
    os.path.join(BASE_DIR, "college_data.json"),
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)


@app.get("/")
def home():
    return FileResponse("index.html")


@app.post("/chat")
def chat(msg: Message):

    text = msg.message.lower().strip()

    # Greetings
    if any(word in text for word in [
        "hi", "hello", "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]):
        return {
            "reply": """Hello 👋 Welcome to MRECW.

I can help you with:

• Principal
• HOD Details
• Courses
• Placements
• Highest Package
• Hostel
• Library
• Contact Details
• Address
• Admissions
• Rankings
"""
        }

    # All HODs
    if text == "hod" or "all hods" in text:
        return {
            "reply": """Department HODs

CSE - Dr. Y. Geetha Reddy

CSE-AIML - Dr. M. Narendar Mulugu

CSE-Data Science - Dr. N. Srinivasa Rao

CSE-Cyber Security - Dr. Yasaswini Vanapalli
"""
        }

    # Search knowledge base
    best_score = 0
    best_answer = None

    for item in data["knowledge"]:

        score = 0

        for keyword in item["keywords"]:

            if keyword.lower() in text:
                score += 1

        if score > best_score:
            best_score = score
            best_answer = item["answer"]

    if best_answer:
        return {"reply": best_answer}

    return {
        "reply": """Sorry, I couldn't find that information.

Try asking:

• Principal
• Chairman
• Courses
• Placements
• Highest Package
• Hostel
• Library
• Contact Number
• Address
• AIML HOD
• CSE HOD
• NAAC Grade
• NIRF Ranking
"""
    }