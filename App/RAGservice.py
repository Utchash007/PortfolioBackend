from haystack import Pipeline


def run_rag(pipe: Pipeline, question: str) -> str:
    result = pipe.run(
        {
            "TextEmbedder": {"text": question},
            "FullTextRetriever": {"query": question},
            "ChatPromptBuilder": {"question": question},
        }
    )
    return result["ChatGenerator"]["replies"][0].text
