#!/usr/bin/env python
import logging
import traceback as tb

from celery import Celery
from ai_platform.config import settings
from ai_platform.task_queue.images_creation import create_image, startup_pipeline
from ai_platform.domain.image_tasks.models import ImageTask
from ai_platform.domain.image_tasks.use_cases import update_image_task

app = Celery(
    "ai-platform",
    broker=settings.REDIS_URL,
    result_backend=settings.REDIS_URL,
    broker_connection_retry_on_startup=True,
)


class ImageTaskPipeline:
    pipe = startup_pipeline()

    @staticmethod
    @app.task(name="generate_image")
    def generate_image(**kwargs):
        image = ImageTask(**kwargs)
        logging.info(f"Executing image creation task: {image.id}")
        try:
            image_file = create_image(ImageTaskPipeline.pipe, image)

            image_file.save(image.image_path)
            image.set_completed()

        except Exception as e:
            stack_trace = tb.format_exc()
            logging.error(f"Error generating image: {repr(e)}: {stack_trace}")
            image.set_failed(reason=repr(e))

        finally:
            logging.info(f"Task finished: {image.id}")
            image.set_completed()
            update_image_task(image)
            return image.url


if __name__ == "__main__":
    app.start()
