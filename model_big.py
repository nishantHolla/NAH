import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from stopwords import stop_words

from transformers import AutoTokenizer, AutoModel
import torch

# Load BERT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load stopwords
stop_words = set(stop_words)

# Function to extract important words (nouns, verbs, adjectives, proper nouns)
def get_important_words(sentence):
    doc = nlp(sentence)
    important_words = [
        token.text
        for token in doc
        if token.pos_ in ["NOUN", "VERB", "ADJ", "PROPN"]
        and token.text.lower() not in stop_words
    ]
    return important_words

# Function to extract named entities (ORG, GPE)
def get_ents(sentence):
    doc = nlp(sentence)
    ents = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "GPE"]]
    return ents

# Function to get embeddings for a list of words using BERT
def get_bert_embeddings(word_list):
    embeddings_dict = {}
    for word in word_list:
        inputs = tokenizer(word, return_tensors="pt")
        outputs = model(**inputs)
        # Use the CLS token (first token in the sequence) for embedding
        embeddings = outputs.last_hidden_state[:, 0, :].squeeze().detach().numpy()
        embeddings_dict[word] = embeddings
    return embeddings_dict

# Function to find similar words based on the input word list
def find_similar_words(word_list, embeddings_dict, top_n=10):
    valid_vectors = [
        embeddings_dict[word] for word in word_list if word in embeddings_dict
    ]
    if len(valid_vectors) == 0:
        return ["No similar words found"]

    # Calculate the average vector
    avg_vector = np.mean(valid_vectors, axis=0)

    # Convert embeddings to NumPy arrays
    all_words = np.array(list(embeddings_dict.keys()))
    all_vectors = np.array(list(embeddings_dict.values()))

    # Calculate cosine similarity between average vector and all vectors
    similarities = cosine_similarity([avg_vector], all_vectors)[0]

    # Get the top N similar words
    top_indices = similarities.argsort()[-top_n:][::-1]
    return all_words[top_indices]

# Function to filter words by POS (keep nouns, proper nouns, adjectives)
def filter_words(word_list):
    filtered_words = []
    for word in word_list:
        doc = nlp(str(word))
        for token in doc:
            if token.pos_ in ["NOUN", "PROPN", "ADJ"] and token.text.lower() not in stop_words:
                filtered_words.append(token.text)
    return filtered_words

# Example usage
def predict(sentence):
    print("Running model for ", sentence)
    # Extract important words and entities
    important_words = get_important_words(sentence.lower())
    ents = get_ents(sentence)

    print(f"Input Sentence: {sentence}")
    
    # Get BERT embeddings for the important words
    bert_embeddings = get_bert_embeddings(important_words)

    # Find similar words
    print(f"Finding words similar to: {important_words}...")
    similar_words = find_similar_words(important_words, bert_embeddings, top_n=10)

    # Remove stopwords from similar words
    similar_words = set(similar_words).difference(stop_words)

    # Filter similar words by POS and combine with entities
    filtered_words = filter_words(list(similar_words))
    
    # Ensure entities do not contain stopwords
    filtered_words += [ent for ent in ents if ent.lower() not in stop_words]
    filtered_words = list(set(filtered_words))

    return filtered_words
