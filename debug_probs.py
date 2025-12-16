import pickle
import nltk
from nltk.stem import WordNetLemmatizer
import os
import pandas as pd

# Load artifacts
with open('chat_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = nltk.word_tokenize(text)
    return ' '.join([lemmatizer.lemmatize(word.lower()) for word in tokens])

queries = [
    "Hello", "Hi", # Greeting (Should be high)
    "I have a fever", # Symptom (Should be high)
    "head hurt", # Vague (Should be medium?)
    "feel bad", # Very vague (Should be medium/low)
    "tell me about aspirin", # Drug (Should be high)
    "wrongqueryblah", # Nonsense (Should be low)
    "chest pain", # Emergency (Should be high)
    "skin rash on leg" # Specific symptom
]

print(f"{'Query':<25} | {'Top Tag':<20} | {'Prob':<6} | {'2nd Tag':<20} | {'2nd Prob'}")
print("-" * 90)

for q in queries:
    processed = preprocess_text(q)
    vec = vectorizer.transform([processed])
    probs = model.predict_proba(vec)[0]
    
    # Get top indices
    top_indices = probs.argsort()[-3:][::-1]
    
    top_tag = model.classes_[top_indices[0]]
    top_prob = probs[top_indices[0]]
    
    sec_tag = model.classes_[top_indices[1]]
    sec_prob = probs[top_indices[1]]
    
    print(f"{q:<25} | {top_tag:<20} | {top_prob:.2f} | {sec_tag:<20} | {sec_prob:.2f}")
