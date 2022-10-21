from typing import List

from fastapi import APIRouter, Header, Depends, HTTPException, status

from api.v1.models import MyAccount, Account, Transaction, Result
from services.accounting import AccountingService, AccountNotFoundException, get_service

router = APIRouter()

@router.get("", response_model=Result)
async def list_accounts(
    service: AccountingService = Depends(get_service),
) -> Result:
    accounts = service.list_accounts()
    return Result(result=[Account(user_id=account.username, balance=account.balance) for account in accounts])

@router.get("/my", response_model=Result)
async def get_my_account(
    x_user: str = Header(), 
    service: AccountingService = Depends(get_service),
    ) -> Result:
    try:
        account = service.get_user_account(x_user)
    except AccountNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    transactions = service.list_account_transactions(account.id)

    return Result(
        result=MyAccount(
            user_id=account.username,
            balance=account.balance,
            transactions=[Transaction(type=t.type, timestamp=t.created_at, description=t.description, amount=t.amount()) for t in transactions],
            ),
        )

