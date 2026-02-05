from typing import Optional
from pymongo import AsyncMongoClient
from beanie import Document, Indexed, init_beanie
from DBQuery.DocumentModel import InitState
from Configs.config import MONGO_URI

async def init():
    client = AsyncMongoClient(
        MONGO_URI
    )
    db = client.Status
    await init_beanie(database=db, document_models=[InitState])

