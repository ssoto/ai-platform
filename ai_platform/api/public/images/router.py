import os.path

from fastapi import APIRouter, Request
from fastapi.responses import Response
from ai_platform.domain.image_tasks.use_cases import afind_image_task_by_id

router = APIRouter(
    prefix="/images",
    tags=["Images"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{image_id}",
    responses={
        200: {
            "content": {"image/png": {}}
        },
        404: {"description": "Image not found"},
    },
    response_class=Response,
)
async def retrieve(request: Request, image_id: str):
    image_task = await afind_image_task_by_id(
        image_id,
        request.app.mongodb["image_tasks"]
    )
    if not os.path.exists(image_task.image_path):
        return Response(
            status_code=404,
            content=f"Image {image_id}.png not found"
        )

    with open(image_task.image_path, "rb") as image_file:
        image_bytes = image_file.read()
    return Response(
        content=image_bytes,
        media_type="image/png"
    )
