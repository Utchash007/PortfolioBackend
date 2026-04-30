import logging
import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from openai import RateLimitError
from pydantic import BaseModel, Field

from DBQuery import Query
from DBQuery.mongoConfig import init
from RAGPipeline import pipeline, Checker
from App.RAGservice import run_rag

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)


class QueryResponse(BaseModel):
    answer: str


async def keepalive_task():
    """Pings Mongo periodically to prevent idle-timeout disconnects on Atlas."""
    logger = logging.getLogger(__name__)
    while True:
        try:
            await Query.getState()
        except Exception:
            logger.warning("Keep-alive ping failed", exc_info=True)
        await asyncio.sleep(60)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init()
    await Checker.checkRAG()
    app.state.pipe = pipeline.build_pipeline()
    task = asyncio.create_task(keepalive_task())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def home():
    return {"message": "Hello, World!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
async def ready():
    state = await Query.getState()
    return {"ready": state == 1}


@app.get("/test")
async def test():
    return await Query.getState()


@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest, request: Request):
    try:
        answer = await asyncio.to_thread(run_rag, request.app.state.pipe, req.question)
    except RateLimitError:
        raise HTTPException(status_code=429, detail="LLM rate limit reached. Please try again later.")
    return QueryResponse(answer=answer)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
