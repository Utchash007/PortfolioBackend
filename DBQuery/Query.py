from DBQuery.DocumentModel import InitState


async def getLatest() -> InitState | None:
    return await InitState.find_all().sort("-createdAt").limit(1).first_or_none()


async def getState() -> int | None:
    result = await getLatest()
    return result.state if result else None


async def addState(file_hash: str) -> None:
    await InitState(state=1, file_hash=file_hash).save()
