import os
import tempfile

from haystack import Pipeline
from haystack.components.builders import ChatPromptBuilder
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.components.joiners import DocumentJoiner
from haystack.dataclasses import ChatMessage
from haystack.utils import Secret
from haystack.components.embedders import HuggingFaceAPITextEmbedder
from haystack_integrations.components.retrievers.mongodb_atlas import (
    MongoDBAtlasEmbeddingRetriever,
    MongoDBAtlasFullTextRetriever,
)
from Configs.config import ConfigService
from RAGPipeline.db import document_store

PIPELINE_YAML = "pipeline.yaml"

system_message = ChatMessage.from_system(
    "You are a software engineer. Answer every question in first person as if you are that person. "
    "Use ONLY the information from the context provided — do not invent or assume anything not stated there. "
    "If the answer is not in the context, say you don't have that information."
)

user_template = """
Context:
{% for document in documents %}
    {{ document.content }}
{% endfor %}

Question: {{ question }}
"""


def _build_pipeline() -> Pipeline:
    pipe = Pipeline()

    pipe.add_component(
        "TextEmbedder",
        HuggingFaceAPITextEmbedder(
            api_type="serverless_inference_api",
            api_params={"model": ConfigService.get_embedding_model()},
            token=Secret.from_env_var("HF_EMBED_TOKEN"),
        ),
    )
    pipe.add_component(
        "VectorRetriever",
        MongoDBAtlasEmbeddingRetriever(document_store=document_store, top_k=5),
    )
    pipe.add_component(
        "FullTextRetriever",
        MongoDBAtlasFullTextRetriever(document_store=document_store, top_k=5),
    )
    pipe.add_component(
        "DocumentJoiner",
        DocumentJoiner(join_mode="reciprocal_rank_fusion"),
    )
    pipe.add_component(
        "ChatPromptBuilder",
        ChatPromptBuilder(
            template=[system_message, ChatMessage.from_user(user_template)],
            required_variables=["documents", "question"],
        ),
    )
    pipe.add_component(
        "ChatGenerator",
        OpenAIChatGenerator(
            api_key=Secret.from_env_var("OPENROUTER_API_KEY"),
            api_base_url=ConfigService.get_api_base_url(),
            model=ConfigService.get_model(),
        ),
    )

    pipe.connect("TextEmbedder.embedding", "VectorRetriever.query_embedding")
    pipe.connect("VectorRetriever", "DocumentJoiner")
    pipe.connect("FullTextRetriever", "DocumentJoiner")
    pipe.connect("DocumentJoiner", "ChatPromptBuilder.documents")
    pipe.connect("ChatPromptBuilder", "ChatGenerator")

    return pipe


def build_pipeline() -> Pipeline:
    if os.path.exists(PIPELINE_YAML):
        with open(PIPELINE_YAML, "r") as f:
            pipe = Pipeline.load(f)
    else:
        pipe = _build_pipeline()
        tmp = PIPELINE_YAML + ".tmp"
        with open(tmp, "w") as f:
            pipe.dump(f)
        os.replace(tmp, PIPELINE_YAML)

    pipe.warm_up()
    return pipe
