from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from .embeddings import get_text_embedder, get_retriever
from .llm import get_llm

template = """
Answer the question based on the following context:

{% for document in documents %}
    {{ document.content }}
{% endfor %}

Question: {{ question }}
"""

def build_pipeline():
    pipe = Pipeline()
    pipe.add_component("TextEmbedder", get_text_embedder())
    pipe.add_component("Retriever", get_retriever())
    pipe.add_component("PromptBuilder", PromptBuilder(template=template, required_variables=["documents", "question"]))
    pipe.add_component("Generator", get_llm())

    pipe.connect("TextEmbedder.embedding", "Retriever.query_embedding")
    pipe.connect("Retriever", "PromptBuilder.documents")
    pipe.connect("PromptBuilder", "Generator")
    return pipe