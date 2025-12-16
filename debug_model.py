import pickle
import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = nltk.word_tokenize(text)
    return ' '.join([lemmatizer.lemmatize(word.lower()) for word in tokens])

def test_model():
    print("Loading artifacts...")
    with open('chat_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Model loaded.")

    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    print("Vectorizer loaded.")

    messages = [
        "Hello", # greeting
        "Find a hospital near New York", # hospital_search
        "Tell me about Aspirin", # drug_search (drug_lookup)
        "I have a fever", # symptom_flu
        "I have a burn on my hand", # injury_general (NEW)
        "who created you?", # meta_bot (NEW)
        "panicking right now", # FAILED in stress test
        "my tummy hurts" # Check variation
    ]

    for msg in messages:
        processed = preprocess_text(msg)
        vectorized = vectorizer.transform([processed])
        prob = model.predict_proba(vectorized)
        max_prob = max(prob[0])
        tag = model.predict(vectorized)[0]
        
        print(f"Input: '{msg}'")
        print(f"Processed: '{processed}'")
        print(f"Tag: {tag}, Prob: {max_prob:.4f}")
        print("-" * 20)

if __name__ == "__main__":
    test_model()
