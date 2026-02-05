from haystack import Document
from haystack.components.preprocessors import DocumentSplitter, DocumentCleaner
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.converters import PyPDFToDocument
from .db import document_store

def ingest_documents(file_path: str):
    # Use PyPDFToDocument to load the PDF file
    converter = PyPDFToDocument()
    conversion_result = converter.run(sources=[file_path])
    docs = conversion_result["documents"]

    # Clean the text (optional but recommended)
    cleaner = DocumentCleaner()
    cleaned_result = cleaner.run(documents=docs)
    cleaned_docs = cleaned_result["documents"]

    # Split the text into chunks
    splitter = DocumentSplitter(split_by="word", split_length=200, split_overlap=20)
    split_result = splitter.run(documents=cleaned_docs)
    split_docs = split_result["documents"]

    # Generate embeddings for the documents
    # note: use the same model as in embeddings.py
    doc_embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
    doc_embedder.warm_up()
    embedding_result = doc_embedder.run(documents=split_docs)
    docs_with_embeddings = embedding_result["documents"]

    # Write documents with embeddings to MongoDB
    document_store.write_documents(docs_with_embeddings)