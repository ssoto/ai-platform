import logging
from fastapi.responses import JSONResponse
from pydantic import Field, BaseModel, field_validator
from fastapi import APIRouter, Request, status, BackgroundTasks
from typing import Optional

from ai_platform.domain.image_tasks.models import ImageTask
from ai_platform.domain.image_tasks.use_cases import create_image_task, afind_image_task_by_id
from ai_platform.domain.image_repository.use_cases import get_image_url
from ai_platform.domain.task_queues.use_cases import send_generation_message


router = APIRouter(
    prefix="/imageTasks",
    tags=["Image Tasks"],
    responses={404: {"description": "Not found"}},
)


class GenerationRequest(BaseModel):
    prompt: str = Field(
        ...,
        title="Prompt to generate the image"
    )
    generation_steps: Optional[int] = Field(
        50,
        title="Number of steps to generate the image. Values between 1 and 999"
    )
    seed: Optional[int] = Field(
        None,
        title="Seed to generate the image"
    )

    @field_validator("generation_steps") # noqa
    @classmethod
    def validate_generation_steps(cls, v):
        if v < 1 or v > 999:
            raise ValueError("Generation steps must be between 1 and 999")
        return v


@router.get("/")
async def retrieve(request: Request, id_task: str):

    result = await afind_image_task_by_id(id_task, request.app.mongodb["image_tasks"])
    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Task not found"}
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=result.dict()
    )


@router.post("/")
async def generate(
        request: Request,
        body: GenerationRequest,
        background_tasks: BackgroundTasks
):
    image_task = ImageTask(
        prompt=body.prompt,
        generation_steps=body.generation_steps,
        seed=body.seed
    )
    # FIXME: this image service is a local endpoint, it should be a service
    image_task.url = get_image_url(image_task.id)
    await create_image_task(
        image_task,
        request.app.mongodb["image_tasks"]
    )
    background_tasks.add_task(
        send_generation_message, image_task, request.app.celery_app,
    )
    logging.info(f"Task {image_task.id} send to the queue")
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=image_task.dict()
    )
