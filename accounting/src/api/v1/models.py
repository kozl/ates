from typing import List, Union
from datetime import datetime

from pydantic import BaseModel, Field

class CreateTaskRequest(BaseModel):
    title: str = Field(..., example="Название задачи")
    description: str = Field(..., example="Содердание задачи")

class Account(BaseModel):
    user_id: str = Field(..., example="Идентификатор пользователя")
    balance: int = Field(..., example="Баланс пользователя")

class Transaction(BaseModel):
    task_id: str = Field(..., example="Идентификатор задачи")
    action: str = Field(..., example="Тип операции")
    timestamp: datetime = Field(..., example="Время операции")
    amount: int = Field(..., example="Сумма операции")

class MyAccount(BaseModel):
    user_id: str = Field(..., example="Идентификатор пользователя")
    transactions: List[Transaction] = Field(..., example="Баланс пользователя")

class Ok(BaseModel):
    ok: bool = Field(..., description="Успешно")

class Result(BaseModel):
    result: Union[Account, List[Account], Ok]