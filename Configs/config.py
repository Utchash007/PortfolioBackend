import os
from dotenv import load_dotenv

load_dotenv()

class ConfigService:
    __OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    __MONGO_URI = os.getenv("MONGO_URI")
    __DB_NAME = os.getenv("DB_NAME")
    __COLLECTION_NAME = os.getenv("COLLECTION_NAME")
    __VECTOR_INDEX = os.getenv("VECTOR_INDEX")
    __FULL_TEXT_SEARCH_INDEX = os.getenv("FULL_TEXT_SEARCH_INDEX")
    __API_BASE_URL = os.getenv("API_BASE_URL")
    __MODEL = os.getenv("MODEL")

    @classmethod
    def get_openrouter_api_key(cls):
        return cls.__OPENROUTER_API_KEY

    @classmethod
    def get_mongo_uri(cls):
        return cls.__MONGO_URI

    @classmethod
    def get_db_name(cls):
        return cls.__DB_NAME

    @classmethod
    def get_collection_name(cls):
        return cls.__COLLECTION_NAME

    @classmethod
    def get_vector_index(cls):
        return cls.__VECTOR_INDEX

    @classmethod
    def get_full_text_search_index(cls):
        return cls.__FULL_TEXT_SEARCH_INDEX

    @classmethod
    def get_api_base_url(cls):
        return cls.__API_BASE_URL

    @classmethod
    def get_model(cls):
        return cls.__MODEL
