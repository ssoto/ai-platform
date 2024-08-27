from pydantic import BaseModel, Field
from ai_platform.domain.image_tasks.models import ImageTask


class ImageTaskMesage(BaseModel):

    image: ImageTask = Field(..., alias="imageTask")

    class Config:
        allow_population_by_field_name = True
        fields = {
            "imageTask": "image"
        }
        json_encoders = {
            ImageTask: lambda v: v.dict(by_alias=True)
        }


class TaskQueueMessage(BaseModel):

    task: ImageTaskMesage = Field(..., alias="taskQueue")

    class Config:
        allow_population_by_field_name = True
        fields = {
            "taskQueue": "task"
        }
        json_encoders = {
            ImageTaskMesage: lambda v: v.dict(by_alias=True)
        }
