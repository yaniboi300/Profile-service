from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI
from app.consumer import start_consumer
import logging

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При запуске сервера создаем фоновую задачу для Consumer
    consumer_task = asyncio.create_task(start_consumer())
    
    yield # Здесь сервер работает и принимает запросы
    
    # При выключении отменяем задачу
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass

app = FastAPI(title="Profile Service", lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "ok"}