# faq_chatbot.py

import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import streamlit as st

# Download NLTK data
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# -----------------------------
# Step 1: Prepare FAQs
# -----------------------------
faqs = {
    "What is your return policy?": "Our return policy allows returns within 30 days of purchase.",
    "How can I track my order?": "You can track your order using the tracking link sent to your email.",
    "Do you offer international shipping?": "Yes, we ship to most countries worldwide.",
    "How can I contact customer support?": "You can contact support via email or our 24/7 chat.",
    "What payment methods do you accept?": "We accept Visa, MasterCard, PayPal, and Apple Pay."
}

faq_questions = list(faqs.keys())
faq_answers = list(faqs.values())

# -----------------------------
# Step 2: Text Preprocessing
# -----------------------------
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    text = text.lower()  # lowercase
    text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(tokens)

preprocessed_questions = [preprocess(q) for q in faq_questions]

# -----------------------------
# Step 3: Chatbot Response Function
# -----------------------------
def get_response(user_input):
    user_input_processed = preprocess(user_input)
    
    # Vectorize FAQ questions + user input
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(preprocessed_questions + [user_input_processed])
    
    # Compute cosine similarity
    similarity = cosine_similarity(vectors[-1], vectors[:-1])
    idx = np.argmax(similarity)
    
    # If similarity is too low, return fallback
    if similarity[0][idx] < 0.2:
        return "Sorry, I don't understand your question."
    
    return faq_answers[idx]

# -----------------------------
# Step 4: Streamlit Chat UI
# -----------------------------
st.title("FAQ Chatbot")
st.write("Ask me anything about our services!")

user_input = st.text_input("Your question:")

if user_input:
    response = get_response(user_input)
    st.text_area("Answer:", value=response, height=100)
