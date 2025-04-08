from pydantic import BaseModel, ConfigDict, Field


class Task(BaseModel):
    title: str
    done: bool = Field(default=False)
    model_config = ConfigDict(from_attributes=True)
