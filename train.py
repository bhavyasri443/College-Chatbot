# ===============================
# STEP 1: Imports
# ===============================
import json
import nltk
import string
import pickle

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression


# ===============================
# STEP 2: Download NLTK resources
# ===============================
nltk.download("stopwords")
nltk.download("wordnet")


# ===============================
# STEP 3: Load intents.json
# ===============================
with open("intents.json", "r", encoding="utf-8") as file:
    data = json.load(file)


# ===============================
# STEP 4: Extract sentences & labels
# ===============================
sentences = []
labels = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        sentences.append(pattern)
        labels.append(intent["tag"])


# ===============================
# STEP 5: Text preprocessing
# ===============================
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def preprocess(text):
    tokens = wordpunct_tokenize(text.lower())
    tokens = [t for t in tokens if t not in string.punctuation]
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words]
    return " ".join(tokens)


# ===============================
# STEP 6: Apply preprocessing
# ===============================
processed_sentences = [preprocess(s) for s in sentences]


# ===============================
# STEP 7: Vectorization (TF-IDF)
# ===============================
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(processed_sentences)


# ===============================
# STEP 8: Encode labels
# ===============================
encoder = LabelEncoder()
y = encoder.fit_transform(labels)


# ===============================
# STEP 9: Train model on FULL dataset
# ===============================
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

print("Model trained on full dataset")


# ===============================
# STEP 10: Save model & tools
# ===============================
pickle.dump(model, open("chatbot_model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))
pickle.dump(encoder, open("label_encoder.pkl", "wb"))

print("Training complete. Model saved successfully.")
