import logging
from fastapi import FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorClient
from ai_platform.api.public.images.router import router as images_router
from ai_platform.sandbox.images_creation import startup_pipeline
from ai_platform.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def initialize_app(app: FastAPI):
    logging.info("Initializing app...")
    # do some initialization here
    startup_pipeline()
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]
    logging.info("App initialized")
    yield
    app.mongodb_client.close()


app = FastAPI(
    title="AI Platform",
    lifespan=initialize_app,
)


@app.get("/health")
async def health(request: Request):
    result = await request.app.mongodb_client.server_info()
    return result

app.include_router(images_router)
