from fastapi import FastAPI
import asyncio
from contextlib import asynccontextmanager
import uvicorn
from DBQuery import Query
from DBQuery.mongoConfig import init
from RAGPipeline import pipeline,Checker
from App.RAGservice import run_rag

pipe = pipeline.build_pipeline()

async def background_task():
    while True:
        await Query.getState()
        await asyncio.sleep(2)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init()  # Initialize Beanie on startup
    await Checker.checkRAG()
    task = asyncio.create_task(background_task())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"message": "Hello, World!"}


@app.get("/test")
async def test():
    return await Query.getState()

@app.post("/query")
def query(question: str):
    return {"answer": run_rag(pipe, question)}
