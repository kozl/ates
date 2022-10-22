from functools import lru_cache
from random import randrange
from typing import List

from fastapi import Depends

from repos.accounts.abstract import AccountsRepo
from repos.accounts.orm import get_account_repo
from repos.accounts.models import Account, Transaction, BillingPeriod, TransactionTypes
from repos.accounts.exceptions import AccountNotFoundException, OpenBillingPeriodNotFoundException, UnexpectedException
from repos.tasks.orm import get_task_repo
from repos.tasks.abstract import TaskRepo
from services.payment import DummyPaymentGateway, get_payment_gateway

class AccountNotFound(Exception):
    pass

class AccountingService:
    def __init__(self, accounts: AccountsRepo, tasks: TaskRepo, payment_gateway: DummyPaymentGateway) -> None:
        self.accounts = accounts
        self.tasks = tasks
        self.payment_gateway = payment_gateway

    def list_accounts(self) -> List[Account]:
        return self.accounts.list_accounts()

    def list_account_transactions(self, account_id: str) -> List[Transaction]:
        return self.accounts.list_account_transactions(account_id)

    def get_user_account(self, username: str) -> Account:
        return self.accounts.get_user_account(username)

    def get_user_transactions(self, username: str) -> List[Transaction]:
        account = self.accounts.get_user_account(username)
        return self.accounts.list_account_transactions(account.id)

    def add_user_account(self, username: str) -> Account:
        return self.accounts.add_user_account(username)

    def create_task(self, task_id: str, assignee: str) -> None:
        fee = randrange(10, 20)
        reward = randrange(20, 40)
        self.tasks.create_task(task_id, assignee, fee, reward)
        try:
            account = self.accounts.get_user_account(assignee)
        except AccountNotFoundException:
            account = self.accounts.add_user_account(assignee)
        
        self.accounts.apply_withdraw_transaction(account.id, TransactionTypes.TASK_ASSIGNED, fee)
    
    def assign_task(self, task_id: str, assignee: str) -> None:
        task = self.tasks.assign_task(task_id, assignee)
        self.accounts.apply_withdraw_transaction(task.assignee, TransactionTypes.TASK_ASSIGNED, task.fee)

    def complete_task(self, task_id: str) -> None:
        task = self.tasks.get_task(task_id)
        self.accounts.apply_deposit_transaction(task.assignee, TransactionTypes.TASK_COMPLETED, task.reward)

    def process_payment(self, username: str) -> None:
        account = self.accounts.get_user_account(username)
        amount_to_pay = self.accounts.close_billing_period(account.id)
        self.payment_gateway.pay(username, amount_to_pay)
  

@lru_cache()
def get_service(
    accounts_repo: AccountsRepo = Depends(get_account_repo),
    tasks_repo: TaskRepo = Depends(get_task_repo),
    payment_gateway = Depends(get_payment_gateway)
) -> AccountingService:
    return AccountingService(
        accounts=accounts_repo,
        tasks=tasks_repo,
        payment_gateway=payment_gateway
    )