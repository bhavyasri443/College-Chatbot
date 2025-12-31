from flask import Flask, render_template, request, jsonify
import json
import pickle
import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize

app = Flask(__name__)

# Load trained model and tools
model = pickle.load(open("chatbot_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
encoder = pickle.load(open("label_encoder.pkl", "rb"))

# Load intents
with open("intents.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# NLP setup
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def preprocess(text):
    tokens = wordpunct_tokenize(text.lower())
    tokens = [t for t in tokens if t not in string.punctuation]
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words]
    return " ".join(tokens)

def get_response(user_input):
    processed = preprocess(user_input)
    vector = vectorizer.transform([processed])
    pred = model.predict(vector)
    intent = encoder.inverse_transform(pred)[0]

    for i in data["intents"]:
        if i["tag"] == intent:
            return i["responses"][0]

    return "Sorry, I didn't understand that."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    reply = get_response(user_msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

