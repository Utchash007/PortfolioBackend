from haystack import Pipeline

def run_rag(pipe: Pipeline, question: str) -> str:
    result = pipe.run({
        "TextEmbedder": {"text": question},
        "PromptBuilder": {"question": question}
    })
    return result["Generator"]["replies"][0]