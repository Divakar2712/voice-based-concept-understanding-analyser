from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st


# ----------------------------------------------------
# Load Sentence-BERT model only once
# ----------------------------------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


# ----------------------------------------------------
# Calculate Semantic Similarity
# ----------------------------------------------------
def calculate_similarity(reference_text, student_text):
    """
    Calculate semantic similarity between
    the reference concept and the student's transcript.
    """

    model = load_model()

    embeddings = model.encode(
        [reference_text, student_text],
        convert_to_tensor=False
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    similarity_percentage = float(round(float(similarity) * 100, 2))

    return similarity_percentage