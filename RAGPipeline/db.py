from haystack.utils import Secret
from haystack_integrations.document_stores.mongodb_atlas import MongoDBAtlasDocumentStore
from Configs.config import *

document_store = MongoDBAtlasDocumentStore(
    mongo_connection_string=Secret.from_token(MONGO_URI),
    database_name=DB_NAME,
    collection_name=COLLECTION_NAME,
    vector_search_index=VECTOR_INDEX,
    full_text_search_index=FULL_TEXT_SEARCH_INDEX,
)