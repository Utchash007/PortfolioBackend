from haystack import Document
from haystack.components.preprocessors import DocumentSplitter, DocumentCleaner
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.converters import PyPDFToDocument
from Configs.config import ConfigService
from .db import document_store

def ingest_documents(file_path: str):
    converter = PyPDFToDocument()
    conversion_result = converter.run(sources=[file_path])
    docs = conversion_result["documents"]

    cleaner = DocumentCleaner()
    cleaned_result = cleaner.run(documents=docs)
    cleaned_docs = cleaned_result["documents"]

    splitter = DocumentSplitter(split_by="word", split_length=200, split_overlap=20)
    split_result = splitter.run(documents=cleaned_docs)
    split_docs = split_result["documents"]

    doc_embedder = SentenceTransformersDocumentEmbedder(model=ConfigService.get_embedding_model())
    doc_embedder.warm_up()
    embedding_result = doc_embedder.run(documents=split_docs)
    docs_with_embeddings = embedding_result["documents"]

    document_store.write_documents(docs_with_embeddings)
