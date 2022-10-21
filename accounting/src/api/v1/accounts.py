from typing import List

from fastapi import APIRouter, Header, Depends, HTTPException, status

from api.v1.models import Task, CreateTaskRequest, Result, Ok
from services.accounts import AccountingService, get_service

router = APIRouter()

@router.get("", response_model=Result)
async def list_accounts(
    x_user: str = Header(), 
    service: AccountingService = Depends(get_service),
) -> Result:
    pass