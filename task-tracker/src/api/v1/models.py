from typing import List, Union

from pydantic import BaseModel, Field

class CreateTaskRequest(BaseModel):
    description: str = Field(..., example="Содердание задачи")

class Task(BaseModel):
    id: str
    description: str = Field(..., description="Содержание задачи")
    status: str = Field(..., description="Статус задачи")
    assignee: str = Field(..., description="Исполнитель задачи")

class Ok(BaseModel):
    ok: bool = Field(..., description="Успешно")

class Result(BaseModel):
    result: Union[Task, List[Task], Ok]