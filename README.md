# MediBot - AI Health Assistant 🏥

MediBot is an intelligent, NLP-powered chatbot designed to provide basic medical information, symptom checking, and real-time utilities like hospital search and drug information lookup. Built with Python (Flask) and a custom Machine Learning model.

![MediBot UI](https://via.placeholder.com/800x400?text=MediBot+Interface+Preview) 
*(Replace with actual screenshot if available)*

## ✨ Key Features

*   **🧠 AI Intent Recognition**: Uses Natural Language Processing (NLTK + TF-IDF + LinearSVC) to understand user queries, including slang and synonyms.
*   **💡 Smart Fallback System**: Instead of generic error messages, the bot suggests potential topics (e.g., *"Did you mean flu symptoms?"*) when it's unsure.
*   **🏥 Real-Time Hospital Search**: Integrates with the **OpenStreetMap API** to find hospitals and clinics in any specified city.
*   **💊 Drug Information**: Connects to the **OpenFDA API** to fetch official purpose and warning labels for medications.
*   **🎨 Modern UI**: Features a beautiful **Glassmorphism** design with a fully functional **Dark Mode**.

## 🚀 Getting Started

### Prerequisites
*   Python 3.8+
*   pip

### Running the Bot

1.  **Train the Brain**:
    You must run the training script first to generate the model (`chat_model.pkl`) and vocabulary.
    ```bash
    python train.py
    ```

2.  **Start the Server**:
    Launch the Flask application.
    ```bash
    python app.py
    ```

3.  **Access**:
    Open your browser and navigate to `http://127.0.0.1:5000`.

## 📂 Project Structure

*   **`app.py`**: Main Flask application server. Handles routing, API logic, and the Smart Fallback mechanism.
*   **`train.py`**: NLP pipeline. Preprocesses text, trains the LinearSVC model, and saves artifacts.
*   **`intents.json`**: The knowledge base. Contains training patterns (user queries) and responses.
*   **`integrations.py`**: Wrapper functions for external APIs (OpenNM & OpenFDA).
*   **`stress_test.py`**: Automated testing script to verify model performance against diverse queries.
*   **`templates/index.html`**: The frontend interface with Dark Mode and animation logic.

## ⚠️ Disclaimer

**MediBot is for educational and demonstration purposes only.** It is **not** a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or qualified health provider.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
