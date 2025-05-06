from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class Task(BaseModel):
    title: str
    done: bool = Field(default=False)
    model_config = ConfigDict(from_attributes=True)
