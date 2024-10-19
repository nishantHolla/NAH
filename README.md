# Hashtag Recommendation System (Browser Extension)

This project is a **Hashtag Recommendation System**, developed as a **browser extension**. It helps users get relevant hashtag recommendations for posts, tweets, or any input text entered into textboxes on the web. The extension works seamlessly in the background, similar to Grammarly, by analyzing the input text and suggesting hashtags to boost reach and relevance.

---

# Team Members

- Nishant Holla - PES1UG23CS401 [Github](https://github.com/nishantHolla)
- Pranav Hemanth - PES1UG23CS433 [Github](https://github.com/Pranavh-2004)
- Pranav Rajesh Narayan - PES1UG23CS435 [Github](https://github.com/prxnav2005)
- Roshini Ramesh - PES1UG23CS488 [Github](https://github.com/roshr22)

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Real-time hashtag recommendations** based on the text input.
- Works across multiple platforms (e.g., Twitter, Instagram, LinkedIn) in any text input field.
- **Intelligent filtering** using BERT embeddings, spaCy models, and GloVe embeddings to recommend relevant hashtags.
- **Named Entity Recognition (NER)** to identify key topics such as organizations or places from the text.
- Integrated **backend API** to analyze input text and suggest hashtags dynamically.
- **Stopword removal and POS filtering** to focus on important terms (nouns, verbs, adjectives, etc.).
- Simple and intuitive UI that mimics the functionality of Grammarly’s suggestions.

---

## How It Works

1. **Input Text Extraction:** The browser extension captures any input text in real-time from a textbox.
2. **Text Analysis:** The backend processes the text using spaCy to extract **important words** and **named entities**.
3. **Embedding Generation:**
   - **BERT** model generates word embeddings for deeper semantic understanding.
   - **GloVe embeddings** provide similarity scores to find related hashtags.
4. **Hashtag Recommendation:**
   - The system filters recommended words based on **POS (Parts of Speech)** tags (e.g., nouns, adjectives).
   - Suggestions include **related words** and **named entities** (ORG, GPE) to make hashtags meaningful.
5. **Interactive Suggestions:**
   - The extension displays recommendations inline, allowing users to click and add hashtags directly.

---

## Technology Stack

### Backend:

- **Python** (FastAPI for building APIs)
- **BERT** (via Huggingface Transformers)
- **GloVe embeddings** for similarity search
- **spaCy** for NLP tasks (NER, POS tagging)
- **scikit-learn** for cosine similarity

### Frontend:

- **Browser Extension** with JavaScript for real-time text extraction
- **HTML/CSS** for UI elements

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-repository/hashtag-recommendation-extension.git
   cd hashtag-recommendation-extension
   ```

2. **Set up Python environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\\Scripts\\activate      # For Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy model:**

   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Load GloVe embeddings:**
   Place the glove.6B.300d.txt file inside the glove/ folder. You can download it from [GloVe](https://nlp.stanford.edu/projects/glove/)

6. **Start the FastAPI server:**

   ```bash
   uvicorn main:app --reload
   ```

7. **Install the browser extension:**

- Go to your browser’s extensions page (e.g., chrome://extensions for Chrome).
- Enable Developer Mode.
- Click on Load Unpacked and select the extension/ folder from this repository.

## Usage

1. After installing the extension, go to any text area on social platforms (e.g., Twitter, Instagram).
2. Start typing your post or tweet.
3. The extension will analyze the text in real-time and recommend hashtags.
4. Click on any recommended hashtag to add it directly to your post.

## API Endpoints

1. /api/ping

- Method: GET
- Description: Health check endpoint to verify the API is running.
- Response:

```json
{
  "status": 200,
  "message": "Ping!"
}
```

2. /api/query/text

- Method: POST
- Description: Accepts input text and returns recommended hashtags.
- Request Body:

```json
{
  "query": "This is an example tweet about artificial intelligence"
}
```

- Response:

```json
{
  "status": 200,
  "message": ["#AI", "#ArtificialIntelligence", "#Technology"]
}
```

---

## Contributing

We welcome contributions! If you’d like to contribute:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Commit your changes (git commit -m 'Add a new feature').
4. Push to the branch (git push origin feature-branch).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments

- [Huggingface Transformers](https://huggingface.co/docs/transformers/index)
- [spaCy](https://spacy.io/)
- [GloVe](https://nlp.stanford.edu/projects/glove/)
