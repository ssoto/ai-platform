import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from ai_platform.api.public.image_tasks.router import router as image_tasks_router
from ai_platform.api.public.images.router import router as images_router
from ai_platform.task_queue.main import app as celery_app
from ai_platform.utils import is_redis_ok, is_mongo_ok
from ai_platform.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)


def initialize_app(app: FastAPI):
    logging.info("Initializing app...")
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]
    app.celery_app = celery_app
    logging.info("App initialized")
    yield
    app.mongodb_client.close()


app = FastAPI(
    title="AI Platform",
    root_path=settings.API_ROOT_PATH,
    debug=True,
    lifespan=initialize_app
)


@app.get("/health")
async def health(request: Request):

    result = {
        "mongodb": await is_mongo_ok(request.app.mongodb_client),
        "redis": is_redis_ok(),
    }
    return JSONResponse(
        content=result,
        status_code=200 if all(result.values()) else 500
    )

app.include_router(image_tasks_router)
app.include_router(images_router)
