from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack_integrations.components.retrievers.mongodb_atlas import MongoDBAtlasEmbeddingRetriever
from Configs.config import ConfigService
from .db import document_store


def get_text_embedder():
    return SentenceTransformersTextEmbedder(model=ConfigService.get_embedding_model())


def get_retriever():
    return MongoDBAtlasEmbeddingRetriever(document_store=document_store)
