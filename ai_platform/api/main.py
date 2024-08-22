import logging
from fastapi import FastAPI
from ai_platform.api.public.images.router import router as images_router
from ai_platform.sandbox.images_creation import startup_pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def initialize_app(app: FastAPI):
    logging.info("Initializing app...")
    # do some initialization here
    startup_pipeline()
    logging.info("App initialized")
    yield


app = FastAPI(
    lifespan=initialize_app,
)

app.include_router(images_router)
