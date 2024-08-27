import logging
from celery import Celery
from ai_platform.domain.image_tasks.use_cases import ImageTask


def send_generation_message(image_task: ImageTask, celery_app: Celery):
    result = celery_app.send_task(
        "generate_image",
        kwargs=image_task.dict(),
        queue="default"
    )
    logging.info(f"Task {result.id} sent to the queue")

