import logging
import random
from uuid import uuid4
from fastapi import APIRouter, BackgroundTasks
from ai_platform.domain.images.models import ImageTask
from ai_platform.sandbox.images_creation import generate_image

# def generate_new_image(image_task: ImageTask):
#     # generate image
#     random_int = random.randint(5, 10)
#     logging.info(f"Generating image in {random_int}s for task {image_task.task_id} with prompt {image_task.prompt}...")
#     time.sleep(random_int)
#     logging.info(f"Image for task {image_task.task_id} generated")


router = APIRouter(
    prefix="/ai-platform/v1/images",
    tags=["images"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def retrieve(id_task: str):
    return ImageTask(
        # XXX: look for the prompt dude
        prompt="prompt",
        task_id=id_task,
        status=random.choice(["processing", "completed", "failed"])
    )


@router.post("/")
async def generate(
        prompt: str,
        background_tasks: BackgroundTasks
) -> ImageTask:
    image_task = ImageTask(
        prompt=prompt,
        task_id=uuid4().__str__(),
        status="processing"
    )
    background_tasks.add_task(generate_image, image_task.prompt, image_task.task_id)
    logging.info(f"Task {image_task.task_id} added to the queue")
    return image_task
