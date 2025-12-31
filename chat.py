import json
import pickle
import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize


# Load trained model and tools
model = pickle.load(open("chatbot_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
encoder = pickle.load(open("label_encoder.pkl", "rb"))

# Load intents
with open("intents.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Preprocessing setup
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def preprocess(text):
    tokens = wordpunct_tokenize(text.lower())
    tokens = [t for t in tokens if t not in string.punctuation]
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words]
    return " ".join(tokens)

# Get response from chatbot
def get_response(user_input):
    processed = preprocess(user_input)
    vector = vectorizer.transform([processed])
    prediction = model.predict(vector)
    intent = encoder.inverse_transform(prediction)[0]

    for i in data["intents"]:
        if i["tag"] == intent:
            return i["responses"][0]

    return "Sorry, I didn't understand that."

# Chat loop
print("🤖 College Chatbot is running! (type 'quit' to exit)")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("Bot: Goodbye! 👋")
        break
    response = get_response(user_input)
    print("Bot:", response)
