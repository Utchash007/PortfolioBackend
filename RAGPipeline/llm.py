from haystack.components.generators import OpenAIGenerator
from haystack.utils import Secret
from Configs.config import ConfigService

def get_llm():
    return OpenAIGenerator(
        api_key=Secret.from_token(ConfigService.get_openrouter_api_key()),
        api_base_url=ConfigService.get_api_base_url(),
        model=ConfigService.get_model()
    )
