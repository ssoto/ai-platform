#!/usr/bin/env python
import logging
import traceback as tb

from celery import Celery
from ai_platform.config import settings
from ai_platform.task_queue.images_creation import create_image, startup_pipeline
from ai_platform.domain.image_tasks.models import ImageTask
from ai_platform.domain.image_tasks.use_cases import update_image_task

logger = logging.getLogger(__name__)
# Singleton pipeline
_pipe = None


app = Celery(
    "ai-platform",
    broker=settings.REDIS_URL,
    result_backend=settings.REDIS_URL,
    broker_connection_retry_on_startup=True,
)


@app.task(
    name="generate_image",
    ignore_result=True,
)
def generate_image(**kwargs):
    logger.info(f"Received message: {kwargs}")
    global _pipe
    if not _pipe:
        _pipe = startup_pipeline()
    image = ImageTask(**kwargs)
    image.set_processing()
    update_image_task(image)

    logger.info(f"Executing image creation task: {image.id}")

    try:
        image_file = create_image(_pipe, image)

        image_file.save(image.image_path)
        image.set_completed()

    except Exception as e:
        stack_trace = tb.format_exc()
        logger.error(f"Error generating image: {repr(e)}: {stack_trace}")
        image.set_failed(reason=repr(e))

    finally:
        logger.info(f"Task finished: {image.id}")
        image.set_completed()
        update_image_task(image)
        return image.url


if __name__ == "__main__":
    app.start()
