from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack_integrations.components.retrievers.mongodb_atlas import MongoDBAtlasEmbeddingRetriever
from .db import document_store

def get_text_embedder():
    return SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")

def get_retriever():
    return MongoDBAtlasEmbeddingRetriever(document_store=document_store)