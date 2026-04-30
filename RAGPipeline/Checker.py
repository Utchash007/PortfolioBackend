import logging

from DBQuery import Query
from .ingestion import ingest_documents

logger = logging.getLogger(__name__)


async def checkRAG():
    if await Query.getState() == 1:
        return
    try:
        ingest_documents("Files/Resume-Shariar-Hasan.pdf")
        logger.info("Ingestion complete")
        await Query.addState()
    except Exception:
        logger.exception("Ingestion failed")
        raise
