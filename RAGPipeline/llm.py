from haystack.components.generators import OpenAIGenerator
from haystack.utils import Secret
from Configs.config import *

def get_llm():
    return OpenAIGenerator(
        api_key=Secret.from_token(OPENROUTER_API_KEY),
        api_base_url=API_BASE_URL,
        model=MODEL
    )