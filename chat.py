import pickle
import nltk
import random
import os
from nltk.stem import WordNetLemmatizer
from colorama import init, Fore, Style

# Initialize Colorama
init(autoreset=True)

lemmatizer = WordNetLemmatizer()

def load_artifacts():
    if not os.path.exists('chat_model.pkl'):
        print(Fore.RED + "Error: Model not found. Please run 'train.py' first.")
        return None, None, None

    with open('chat_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    
    with open('tag_map.pkl', 'rb') as f:
        tag_map = pickle.load(f)
        
    return model, vectorizer, tag_map

def preprocess_text(text):
    tokens = nltk.word_tokenize(text)
    return ' '.join([lemmatizer.lemmatize(word.lower()) for word in tokens])

def get_response(user_input, model, vectorizer, tag_map):
    processed_input = preprocess_text(user_input)
    vectorized_input = vectorizer.transform([processed_input])
    
    # Predict tag
    probability = model.predict_proba(vectorized_input)
    index = model.predict(vectorized_input)[0]
    max_prob = max(probability[0])

    if max_prob < 0.5:
        return "I'm sorry, I didn't quite understand that. Could you describe your symptoms differently?"
    
    tag = index
    responses = tag_map.get(tag, ["I'm not sure how to help with that."])
    return random.choice(responses)

def main():
    model, vectorizer, tag_map = load_artifacts()
    if not model:
        return

    print(Fore.CYAN + "="*60)
    print(Fore.CYAN + "          AI MEDICAL CHATBOT (Python NLP Prototype)")
    print(Fore.CYAN + "="*60)
    print(Fore.YELLOW + "DISCLAIMER: This bot is for demonstration only.")
    print(Fore.YELLOW + "It is NOT a substitute for professional medical advice.")
    print(Fore.YELLOW + "If you have a medical emergency, call 911 immediately.")
    print(Fore.CYAN + "="*60)
    print("\n" + Fore.GREEN + "Bot: Hello! How can I help you today? (Type 'quit' to exit)")

    while True:
        try:
            user_input = input(Fore.WHITE + "You: ")
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print(Fore.GREEN + "Bot: Take care! Goodbye.")
                break
            
            if not user_input.strip():
                continue

            response = get_response(user_input, model, vectorizer, tag_map)
            print(Fore.GREEN + f"Bot: {response}")
        
        except KeyboardInterrupt:
            print("\n" + Fore.GREEN + "Bot: Goodbye!")
            break

if __name__ == "__main__":
    main()
