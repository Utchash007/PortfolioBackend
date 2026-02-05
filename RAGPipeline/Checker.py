
from DBQuery import Query
from .ingestion import ingest_documents
async def checkRAG():
    if await Query.getState() == 1:
        return
    try:
        ingest_documents("Files/Resume-Shariar-Hasan.pdf")
        print("==============INGESTION COMPLETE==============")
        await Query.addState()
    except Exception as e:
        print(e)
    
