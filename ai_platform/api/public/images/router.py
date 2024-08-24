import logging
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request, status, BackgroundTasks
from fastapi.encoders import jsonable_encoder

from ai_platform.domain.images.models import ImageTask
from ai_platform.sandbox.images_creation import generate_image
from ai_platform.domain.images.use_cases import create_image_task, find_image_task_by_id


router = APIRouter(
    prefix="/ai-platform/v1/images",
    tags=["images"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def retrieve(request: Request, id_task: str):

    result = await find_image_task_by_id(id_task, request.app.mongodb["image_tasks"])
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Task not found"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result.dict())


@router.post("/")
async def generate(
        request: Request,
        prompt: str,
        background_tasks: BackgroundTasks
):
    prompt = jsonable_encoder(prompt)

    image_task = ImageTask(
        prompt=prompt,
        status="processing"
    )
    await create_image_task(image_task, request.app.mongodb["image_tasks"])

    background_tasks.add_task(generate_image, image_task)
    logging.info(f"Task {image_task.id} added to the queue")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=image_task.dict())
