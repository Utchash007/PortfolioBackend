import hashlib
import logging

from DBQuery import Query
from .ingestion import ingest_documents

logger = logging.getLogger(__name__)

RESUME_PATH = "Files/Resume-Shariar-Hasan.pdf"


def _file_hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


async def checkRAG():
    current_hash = _file_hash(RESUME_PATH)
    latest = await Query.getLatest()

    if latest and latest.state == 1 and latest.file_hash == current_hash:
        return

    if latest and latest.file_hash != current_hash:
        logger.info("Resume file changed — re-ingesting")

    try:
        ingest_documents(RESUME_PATH)
        logger.info("Ingestion complete")
        await Query.addState(file_hash=current_hash)
    except Exception:
        logger.exception("Ingestion failed")
        raise
