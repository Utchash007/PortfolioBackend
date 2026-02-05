from bson import ObjectId
from DBQuery.DocumentModel import InitState

async def getState():
    result = await InitState.find_all().sort("-createdAt").limit(1).first_or_none()
    return result.state if result else None

async def addState():
    result = await InitState(state=1).save()
    return True