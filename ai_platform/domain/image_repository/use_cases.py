import logging
from pymongo import MongoClient

from ai_platform.domain.image_tasks.models import ImageTask
from ai_platform.config import settings


def update_image_task(image_task: ImageTask):
    client = None
    try:
        client = MongoClient(settings.DB_URL)
        collection = client[settings.DB_NAME]["image_tasks"]
        collection.update_one(
            {"_id": image_task.id},
            {"$set": image_task.dict(by_alias=True)}
        )
    except Exception as e:
        logging.error(f"Error updating image task: {e}")
        client.close()


def get_image_url(image_id: str):
    # FIXME: this is a temporary fix
    host = f"{settings.HOST}:{settings.PORT}"
    return f"http://{host}{settings.API_ROOT_PATH}/images/{image_id}"
