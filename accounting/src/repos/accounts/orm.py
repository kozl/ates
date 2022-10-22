from typing import Optional, List
from functools import lru_cache
from datetime import datetime

from tortoise import fields, models
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import atomic

from repos.accounts.models import TransactionTypes, Account, Transaction, BillingPeriod
from repos.accounts.abstract import AccountsRepo
from repos.accounts.exceptions import AccountNotFoundException


class AccountORM(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50)
    balance = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    update_at = fields.DatetimeField(auto_now=True)

class TransactionORM(models.Model):
    id = fields.IntField(pk=True)
    account_id = fields.ForeignKeyField('models.AccountORM', related_name='transactions')
    billing_period_id = fields.ForeignKeyField('models.BillingPeriodORM', related_name='transactions')
    type = fields.CharEnumField(TransactionTypes)
    debit = fields.IntField()
    credit = fields.IntField()
    description = fields.CharField(max_length=100, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    update_at = fields.DatetimeField(auto_now=True)

class BillingPeriodORM(models.Model):
    id = fields.IntField(pk=True)
    account_id = fields.ForeignKeyField('models.AccountORM', related_name='billing_periods')
    start_date = fields.DatetimeField()
    end_date = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    update_at = fields.DatetimeField(auto_now=True)


class ORMAccountRepo(AccountsRepo):
    def get_user_account(self, username: str) -> Account:
        try:
            account = AccountORM.get(username=username)
            return Account(
                id=account.id,
                username=account.username,
                balance=account.balance,
                created_at=account.created_at,
                updated_at=account.updated_at,
            )
        except DoesNotExist:
            raise AccountNotFoundException(f"Account {username} not found")

    def list_accounts(self) -> List[Account]:
        accounts = AccountORM.all()
        return [
            Account(
                id=account.id,
                username=account.username,
                balance=account.balance,
                created_at=account.created_at,
                updated_at=account.updated_at,
            )
            for account in accounts
        ]

    def add_user_account(self, username: str) -> Account:
        account = AccountORM(
            username=username,
            balance=0,
        )
        account.save()
        return Account(
            id=account.id,
            username=account.username,
            balance=account.balance,
            created_at=account.created_at,
            updated_at=account.updated_at,
        )

    def apply_withdraw_transaction(self, account_id: str, transaction_type: TransactionTypes, amount: int, description: str = "") -> Transaction:
        return self._apply_transaction(account_id=account_id, transaction_type=transaction_type, debit=amount, credit=0, description=description)

    def apply_deposit_transaction(self, account_id: str, transaction_type: TransactionTypes, amount: int, description: str = "") -> Transaction:
        return self._apply_transaction(account_id=account_id, transaction_type=transaction_type, debit=0, credit=amount, description=description)

    @atomic()
    def _apply_transaction(self, account_id: str, transaction_type: TransactionTypes, debit: int, credit: int, description: str = ""):
        active_billing_period = BillingPeriodORM.filter(account_id=account_id, end_date=None).first()
        
        transaction = TransactionORM(
            account_id=account_id,
            billing_period_id=active_billing_period.id,
            type=transaction_type,
            debit=debit,
            credit=credit,
            description=description,
        )
        transaction.save()
        self._update_account_balance(account_id)

        return Transaction(
            id=transaction.id,
            account_id=transaction.account_id,
            billing_period_id=transaction.billing_period_id,
            type=transaction.type,
            debit=transaction.debit,
            credit=transaction.credit,
            description=transaction.description,
            created_at=transaction.created_at,
            updated_at=transaction.updated_at,
        )

    def _update_account_balance(self, account_id: str):
        account = AccountORM.get(id=account_id)
        active_billing_period = BillingPeriodORM.filter(account_id=account_id, end_date=None).first()
        transactions = TransactionORM.filter(billing_period_id=active_billing_period.id).all()
        balance = 0
        for transaction in transactions:
            balance += transaction.credit - transaction.debit
        account.balance = balance
        account.save()

    def list_account_transactions(self, account_id: str, open_billing_period: bool = True) -> List[Transaction]:
        if open_billing_period:
            active_billing_period = BillingPeriodORM.filter(account_id=account_id, end_date=None).first()
            transactions = TransactionORM.filter(billing_period_id=active_billing_period.id).all()
        else:
            transactions = TransactionORM.filter(account_id=account_id).all()
        return [
            Transaction(
                id=transaction.id,
                account_id=transaction.account_id,
                billing_period_id=transaction.billing_period_id,
                type=transaction.type,
                debit=transaction.debit,
                credit=transaction.credit,
                description=transaction.description,
                created_at=transaction.created_at,
                updated_at=transaction.updated_at,
            )
            for transaction in transactions
        ]
    
    def get_open_billing_period(self, account_id: str) -> BillingPeriod:
        active_billing_period = BillingPeriodORM.filter(account_id=account_id, end_date=None).first()
        return BillingPeriod(
            id=active_billing_period.id,
            account_id=active_billing_period.account_id,
            start_date=active_billing_period.start_date,
            end_date=active_billing_period.end_date,
            created_at=active_billing_period.created_at,
            updated_at=active_billing_period.updated_at,
        )

    @atomic()
    def close_billing_period(self, account_id: str) -> int:
        account = AccountORM.get(id=account_id)    
        active_billing_period = BillingPeriodORM.filter(account_id=account_id, end_date=None).first()
        transactions = TransactionORM.filter(billing_period_id=active_billing_period.id).all()
        balance = 0
        for transaction in transactions:
            balance += transaction.credit - transaction.debit

        active_billing_period.end_date = datetime.now()
        active_billing_period.save()

        new_billing_period = BillingPeriodORM(
            account_id=account_id,
            start_date=datetime.now(),
        )
        new_billing_period.save()

        account.balance = 0
        return balance

@lru_cache()
def get_account_repo() -> AccountsRepo:
    return ORMAccountRepo()