from pydantic import BaseModel, Field


class ImageTask(BaseModel):
    prompt: str = Field(..., title="Prompt to generate the image", description="Prompt to generate the image")
    task_id: str = Field(..., title="Task ID", description="Task ID")
    status: str = Field(..., title="Task status", description="Task status")
