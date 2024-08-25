import logging

from pymongo import MongoClient

from ai_platform.domain.image_tasks.models import ImageTask
from ai_platform.config import settings


async def create_image_task(image_task: ImageTask, db_collection):
    return await db_collection.insert_one(image_task.dict(by_alias=True))


async def afind_image_task_by_id(id_task: str, db_collection):
    result = await db_collection.find_one({"_id": id_task})
    if result:
        return ImageTask(**result)
    return None


def find_image_task_by_id(id_task: str, db_collection):
    result = db_collection.find_one({"_id": id_task})
    if result:
        return ImageTask(**result)
    return None


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
