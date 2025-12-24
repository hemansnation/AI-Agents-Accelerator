from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
    )
