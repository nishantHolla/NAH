import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from stopwords import stop_words  # Assuming this is a custom stopword list

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

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

# Function to load selected GloVe embeddings into memory
def load_glove_embeddings(file_path, word_list=None):
    embeddings_dict = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            values = line.split()
            word = values[0]
            if word_list is None or word in word_list:
                vector = np.asarray(values[1:], "float32")
                embeddings_dict[word] = vector
    return embeddings_dict

# Function to find similar words based on the input word list
def find_similar_words(word_list, embeddings_dict, top_n=10):
    valid_vectors = [embeddings_dict[word] for word in word_list if word in embeddings_dict]
    if not valid_vectors:
        return []

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
if __name__ == "__main__":
    # Example sentence
    sentence = """
Researchers at the Centre for Nano Science and Engineering (CeNSE) have developed a brain-inspired computing platform that can store and process data in 16,500 conductance states within a molecular film. Published in the journal Nature, this breakthrough represents a huge step forward over traditional digital computers in which data storage and processing are limited to just two states.
The team tapped into tiny molecular movements to design a highly precise and efficient neuromorphic accelerator, which can be seamlessly integrated with silicon circuits to boost their performance and energy efficiency.
Such a platform could potentially bring complex AI tasks, like training LLMs, to personal devices like laptops and smartphones, taking us closer to democratising the development of AI tools. Working in Apple
    """
    
    # Extract important words and entities
    important_words = get_important_words(sentence.lower())
    ents = get_ents(sentence)

    # Load GloVe embeddings
    glove_file = "glove/glove.6B.300d.txt"
    glove_embeddings = load_glove_embeddings(glove_file)

    # Find similar words
    # print(f"Finding words similar to {important_words}...")
    similar_words = find_similar_words(important_words, glove_embeddings, top_n=10)
    similar_words = set(similar_words).difference(stop_words)

    # Filter similar words and combine with entities
    filtered_words = filter_words(list(similar_words))
    filtered_words += ents
    filtered_words = list(set(filtered_words))

    print("Filtered words:", filtered_words)

