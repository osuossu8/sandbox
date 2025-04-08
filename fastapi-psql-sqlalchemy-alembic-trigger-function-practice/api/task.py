from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Task(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    title: str
    done: bool = Field(default=False)
    model_config = ConfigDict(from_attributes=True)
