from flask import Flask, render_template, request, jsonify
import pickle
import nltk
import os
import random
import re
from nltk.stem import WordNetLemmatizer
from integrations import get_drug_info, get_hospitals

app = Flask(__name__)

lemmatizer = WordNetLemmatizer()
model = None
vectorizer = None
tag_map = None

def load_artifacts():
    global model, vectorizer, tag_map
    if not os.path.exists('chat_model.pkl'):
        return False

    with open('chat_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    
    with open('tag_map.pkl', 'rb') as f:
        tag_map = pickle.load(f)
    return True

def preprocess_text(text):
    tokens = nltk.word_tokenize(text)
    return ' '.join([lemmatizer.lemmatize(word.lower()) for word in tokens])

def extract_drug_name(user_input):
    # Simple regex to catch common "drug" queries. In a real app, use NER (Spacy/Bert)
    # Patterns: "side effects of X", "tell me about X", "what is X"
    match = re.search(r'(?:of|about|is|drug)\s+([a-zA-Z]+)', user_input, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def extract_city(user_input):
    # Simple regex to extract city after "in", "at", or "near"
    match = re.search(r'(?:in|at|near)\s+([a-zA-Z\s]+)', user_input, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def get_readable_tag(tag):
    """Converts a tag like 'symptom_flu' to 'Flu Symptoms'."""
    return tag.replace('_', ' ').title()

def get_bot_response(user_input):
    if not model:
        return "Error: Brain not loaded."

    processed_input = preprocess_text(user_input)
    vectorized_input = vectorizer.transform([processed_input])
    
    # Predict probabilities for all classes
    probabilities = model.predict_proba(vectorized_input)[0]
    
    # Get top 3 predictions
    top_indices = probabilities.argsort()[-3:][::-1]
    top_probs = probabilities[top_indices]
    top_tags = model.classes_[top_indices]
    
    max_prob = top_probs[0]
    best_tag = top_tags[0]
    
    # Logic for Smart Fallback
    # Case 1: Low confidence (Complete confusion)
    if max_prob < 0.15: 
        return ("I'm not sure I understand. I can help with:<br>"
                "💊 **Drugs** (e.g. 'About Aspirin')<br>"
                "🏥 **Hospitals** (e.g. 'Hospital near me')<br>"
                "🩺 **Symptoms** (e.g. 'I have a fever')")
    
    # Case 2: Medium confidence (Ambiguity - Suggest options)
    # Lowered threshold to 0.35 because calibrated probabilities are conservative
    elif max_prob < 0.35:
        suggestions = ""
        for i in range(len(top_tags)):
            # Only suggest if reasonable probability (> 0.08) to improve relevance
            if top_probs[i] > 0.08: 
                readable = get_readable_tag(top_tags[i])
                suggestions += f"- {readable}<br>"
        
        # If no suggestions passed the filter, fallback to generic
        if not suggestions:
            return ("I'm not sure I understand. I can help with:<br>"
                "💊 **Drugs** (e.g. 'About Aspirin')<br>"
                "🏥 **Hospitals** (e.g. 'Hospital near me')<br>"
                "🩺 **Symptoms** (e.g. 'I have a fever')")

        return (f"I'm not quite sure, but did you mean one of these?<br><br>"
                f"{suggestions}<br>"
                f"Please try rephrasing your question.")

    # Case 3: High confidence (Proceed as normal)
    tag = best_tag
    
    # INTEGRATION: Check for Drug Lookup
    if tag == "drug_lookup":
        drug_name = extract_drug_name(user_input)
        if drug_name:
            info = get_drug_info(drug_name)
            if info["found"]:
                return f"**{info['name'].upper()}Info:**<br>Purpose: {info['purpose']}<br><br>⚠️ Warnings: {info['warnings']}"
            else:
                return f"I couldn't find specific FDA info for '{drug_name}'. Please check the spelling."
        else:
             return "Please specify the drug name (e.g., 'Advise on Aspirin')."

    # INTEGRATION: Check for Hospital Search
    if tag == "hospital_search":
        city = extract_city(user_input)
        if city:
            info = get_hospitals(city)
            if info["found"]:
                response = f"**Hospitals near {city}:**<br>"
                for hospital in info['hospitals']:
                    response += f"🏥 {hospital['name']}<br>"
                response += f"<a href='https://www.openstreetmap.org/search?query=hospitals+in+{city}' target='_blank'>View on Map</a>"
                return response
            else:
                return f"I couldn't find hospitals in '{city}'."
        else:
            return "Please specify the city (e.g., 'Hospitals in Boston')."

    responses = tag_map.get(tag, ["I'm not sure how to help with that."])
    return random.choice(responses)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def chat_api():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "Please say something."})
    
    response = get_bot_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    if load_artifacts():
        print("Model loaded successfully.")
    else:
        print("Model not found. Run train.py first.")
    
    app.run(debug=True, port=5000)
