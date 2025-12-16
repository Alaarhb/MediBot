import json
import nltk
import pickle
import numpy as np
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Initialize Lemmatizer
lemmatizer = WordNetLemmatizer()

def download_nltk_data():
    """Download necessary NLTK data."""
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('tokenizers/punkt_tab')
        nltk.data.find('corpora/wordnet')
    except LookupError:
        print("Downloading NLTK data...")
        nltk.download('punkt')
        nltk.download('punkt_tab')
        nltk.download('wordnet')

def preprocess_text(text):
    """Tokenize and lemmatize text."""
    tokens = nltk.word_tokenize(text)
    return ' '.join([lemmatizer.lemmatize(word.lower()) for word in tokens])

def train_model():
    download_nltk_data()

    # Load Intents
    with open('intents.json', 'r') as file:
        data = json.load(file)

    patterns = []
    tags = []
    tag_map = {}

    print("Processing data...")
    for intent in data['intents']:
        for pattern in intent['patterns']:
            # Create a corpus of patterns
            patterns.append(preprocess_text(pattern))
            tags.append(intent['tag'])
        
        tag_map[intent['tag']] = intent['responses']

    # Vectorization (TF-IDF)
    # n-gram range (1,2) allows the model to capture phrases like "near me" or "chest pain"
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X = vectorizer.fit_transform(patterns)
    y = tags

    # Train Model
    print("Training model...")
    from sklearn.svm import LinearSVC
    from sklearn.calibration import CalibratedClassifierCV

    # Train Model
    print("Training model...")
    # Use LinearSVC for better performance on text data, with probability calibration
    svc = LinearSVC()
    model = CalibratedClassifierCV(svc, method='sigmoid')
    model.fit(X, y)

    # Evaluate (simple check on training data)
    score = model.score(X, y)
    print(f"Model trained with accuracy on training set: {score:.2f}")

    # Save Artifacts
    print("Saving model and vectorizer...")
    with open('chat_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    
    with open('tag_map.pkl', 'wb') as f:
        pickle.dump(tag_map, f)

    print("Training complete! Run 'chat.py' to talk to the bot.")

if __name__ == "__main__":
    train_model()
