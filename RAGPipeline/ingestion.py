from haystack import Pipeline
from haystack.components.converters import PyPDFToDocument
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.embedders import HuggingFaceAPIDocumentEmbedder
from haystack.utils import Secret
from haystack.components.writers import DocumentWriter
from Configs.config import ConfigService
from RAGPipeline.db import document_store


def ingest_documents(file_path: str) -> None:
    pipe = Pipeline()

    pipe.add_component("Converter", PyPDFToDocument())
    pipe.add_component("Cleaner", DocumentCleaner())
    pipe.add_component(
        "Splitter",
        DocumentSplitter(split_by="word", split_length=200, split_overlap=20),
    )
    pipe.add_component(
        "Embedder",
        HuggingFaceAPIDocumentEmbedder(
            api_type="serverless_inference_api",
            api_params={"model": ConfigService.get_embedding_model()},
            token=Secret.from_token(ConfigService.get_hf_embed_token()),
        ),
    )
    pipe.add_component("Writer", DocumentWriter(document_store=document_store))

    pipe.connect("Converter", "Cleaner")
    pipe.connect("Cleaner", "Splitter")
    pipe.connect("Splitter", "Embedder")
    pipe.connect("Embedder", "Writer")

    pipe.warm_up()
    pipe.run({"Converter": {"sources": [file_path]}})
