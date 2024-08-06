import joblib
from gensim.models import Word2Vec
import numpy as np
from gensim.utils import simple_preprocess

# Loading and Using the Model and Classifier
# =============================================
# Load the Word2Vec model, classifier, and label encoder
_word2vec = 'mav_structure/word2vec.model'
_classifier = 'mav_structure/classifier.joblib'
_label_encoder = 'mav_structure/label_encoder.joblib'
word2vec_model = Word2Vec.load(_word2vec)
classifier = joblib.load(_classifier)
label_encoder = joblib.load(_label_encoder)


# Function to convert query to Word2Vec embedding
def get_embedding(query):
    tokens = simple_preprocess(query)
    vectors = [word2vec_model.wv[token] for token in tokens if token in word2vec_model.wv]
    if not vectors:
        return np.zeros(word2vec_model.vector_size)
    return np.mean(vectors, axis=0)


# Function to classify the intent of a user query
def classify_intent(user_query: str) -> str:
    embedding = get_embedding(user_query).reshape(1, -1)
    intent_index = classifier.predict(embedding)[0]
    return label_encoder.inverse_transform([intent_index])[0]

