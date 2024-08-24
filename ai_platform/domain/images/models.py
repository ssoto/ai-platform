from datetime import datetime
from uuid import uuid4
from typing import Optional
from pydantic import BaseModel, Field, model_validator, ConfigDict


NOW_FACTORY = datetime.now


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

    COMPLETED = "completed"
    PROCESSING = "processing"
    FAILED = "failed"

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
        ...,
        title="Task status",
        description="Task status"
    )
    reason: Optional[str] = Field(
        default=None,
        title="Reason of failure",
        description="Reason of failure"
    )

    class Config:
        populate_by_name = True
        json_encoders = {
            uuid4: str,
        }

    def set_completed(self):
        self.status = self.COMPLETED

    def set_processing(self):
        self.status = self.PROCESSING

    def set_failed(self, reason: str):
        self.status = self.FAILED
        self.reason = reason
