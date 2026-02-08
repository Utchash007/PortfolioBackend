from haystack.utils import Secret
from haystack_integrations.document_stores.mongodb_atlas import MongoDBAtlasDocumentStore
from Configs.config import ConfigService

document_store = MongoDBAtlasDocumentStore(
    mongo_connection_string=Secret.from_token(ConfigService.get_mongo_uri()),
    database_name=ConfigService.get_db_name(),
    collection_name=ConfigService.get_collection_name(),
    vector_search_index=ConfigService.get_vector_index(),
    full_text_search_index=ConfigService.get_full_text_search_index(),
)
