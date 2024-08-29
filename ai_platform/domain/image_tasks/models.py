from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import uuid4
from pydantic import BaseModel, Field, model_validator, ConfigDict


NOW_FACTORY = datetime.now
NOT_STARTED = "not_started"
COMPLETED = "completed"
PROCESSING = "processing"
FAILED = "failed"

HERE = Path(__file__).resolve().parent
PROJECT_PATH = HERE.parent.parent.parent
IMAGES_PATH = PROJECT_PATH / "images"


class CreatedUpdatedAt:
    """Created and updated at mixin that automatically updates updated_at field."""

    created_at: datetime = Field(default_factory=NOW_FACTORY)
    updated_at: datetime = Field(default_factory=NOW_FACTORY)

    model_config = ConfigDict(
        validate_assignment=True,
    )

    @classmethod
    @model_validator(mode="after")
    def update_updated_at(cls, obj: "CreatedUpdatedAt") -> "CreatedUpdatedAt":
        """Update updated_at field."""
        # must disable validation to avoid infinite loop
        obj.model_config["validate_assignment"] = False

        # update updated_at field
        obj.updated_at = NOW_FACTORY()

        # enable validation again
        obj.model_config["validate_assignment"] = True
        return obj


class ImageTask(BaseModel):

    prompt: str = Field(
        ...,
        title="Prompt to generate the image",
        description="Prompt to generate the image"
    )
    id: str = Field(
        ...,
        title="Task ID",
        default_factory=lambda: uuid4().__str__(),
        description="Task ID",
        alias="_id"
    )
    status: str = Field(
        default=NOT_STARTED,
        title="Task status",
        description="Task status"
    )
    reason: Optional[str] = Field(
        None,
        title="Reason of failure",
        description="Reason of failure"
    )
    generation_steps: int = Field(
        50,
        title="Number of steps to generate the image",
        description="Number of steps to generate the image"
    )
    seed: Optional[int] = Field(
        None,
        title="Seed to generate the image",
        description="Seed to generate the image"
    )
    url: str = Field(
        None,
        title="URL to download the image",
        description="URL to download the image"
    )

    class Config:
        populate_by_name = True
        json_encoders = {
            uuid4: str,
        }

    def set_completed(self):
        self.status = COMPLETED

    def set_processing(self):
        self.status = PROCESSING

    def set_failed(self, reason: str):
        self.status = FAILED
        self.reason = reason

    @property
    def image_path(self) -> str:
        return (IMAGES_PATH / f"{self.id}.png").__str__()
