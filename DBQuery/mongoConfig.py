from typing import Optional
from pymongo import AsyncMongoClient
from beanie import Document, Indexed, init_beanie
from DBQuery.DocumentModel import InitState
from Configs.config import ConfigService

async def init():
    client = AsyncMongoClient(
        ConfigService.get_mongo_uri()
    )
    db = client.Status
    await init_beanie(database=db, document_models=[InitState])
