from datetime import datetime
from typing import List
from functools import lru_cache

from repos.accounts.abstract import AccountsRepo
from repos.accounts.exceptions import AccountNotFoundException, OpenBillingPeriodNotFoundException, UnexpectedException
from repos.accounts.models import Account, Transaction, BillingPeriod, TransactionTypes

class InMemoryAccountRepo(AccountsRepo):
    def __init__(self, 
    initial_accounts: List[Account] = [], 
    initial_transactions: List[Transaction] = [],
    initial_billing_periods: List[BillingPeriod] = []) -> None:
        self.storage = {
            "accounts": initial_accounts,
            "transactions": initial_transactions,
            "billing_periods": initial_billing_periods
        }

        for account in self.storage["accounts"]:
            self._update_account_balance(account.id, self._account_balance(account.id))

    def get_user_account(self, username: str) -> Account:
        for account in self.storage["accounts"]:
            if account.username == username:
                return account
        raise AccountNotFoundException

    def list_accounts(self) -> List[Account]:
        return self.storage["accounts"]

    def _get_user_account_by_id(self, account_id: str) -> Account:
        for account in self.storage["accounts"]:
            if account.id == account_id:
                return account
        raise AccountNotFoundException

    def _account_balance(self, account_id: str):
        balance = 0
        transactions = self.list_account_transactions(account_id)
        for tr in transactions:
            balance += tr.debit
            balance -= tr.credit
        return balance

    def add_user_account(self, username: str) -> Account:
        try:
            self.get_user_account(username)
        except AccountNotFoundException:
            account = Account(id=str(len(self.storage["accounts"]) + 1), username=username, balance=0, created_at=datetime.now(), updated_at=datetime.now())
            self.storage["accounts"].append(account)
            return account
        raise UnexpectedException

    def _update_user_account(self, account: Account) -> Account:
        for idx, acc in enumerate(self.storage["accounts"]):
            if acc.id == account.id:
                self.storage["accounts"][idx] = account
                return account
        raise UnexpectedException

    def _update_account_balance(self, account_id: str, balance: int) -> Account:
        account = self._get_user_account_by_id(account_id)
        account.balance = balance
        return self._update_user_account(account)

    def apply_withdraw_transaction(self, account_id: str, transaction_type: TransactionTypes, amount: int, description: str = "") -> Transaction:
        billing_period = self.get_open_billing_period(account_id)
        transaction = Transaction(
            id=str(len(self.storage["transactions"]) + 1),
            account_id=account_id,
            billing_period_id=billing_period.id,
            type=transaction_type.value,
            description=description,
            debit=0,
            credit=amount,
            created_at=datetime.now(),
            )
        self.storage["transactions"].append(transaction)

        self._update_account_balance(account_id, self._account_balance(account_id))
        return transaction

    def apply_debit_transaction(self, account_id: str, transaction_type: TransactionTypes, amount: int, description: str = "") -> Transaction:
        billing_period = self.get_open_billing_period(account_id)
        transaction = Transaction(
            id=str(len(self.storage["transactions"]) + 1),
            account_id=account_id,
            billing_period_id=billing_period.id,
            type=transaction_type.value,
            description=description,
            debit=amount,
            credit=0,
            created_at=datetime.now(),
            )
        self.storage["transactions"].append(transaction)

        self._update_account_balance(account_id, self._account_balance(account_id))
        return transaction

    def list_account_transactions(self, account_id: str, open_billing_period: bool = True) -> List[Transaction]:
        transactions = [tr for tr in self.storage["transactions"] if tr.account_id == account_id]
        if not open_billing_period:
            return transactions
        
        billing_period = self.get_open_billing_period(account_id)
        return [tr for tr in transactions if tr.billing_period_id == billing_period.id]

    def get_open_billing_period(self, account_id: str) -> BillingPeriod:
        billing_periods = [bp for bp in self.storage["billing_periods"] if bp.account_id == account_id]
        for bp in billing_periods:
            if bp.end_date is None:
                return bp
        raise OpenBillingPeriodNotFoundException

    def close_billing_period(self, account_id: str) -> int:
        bp = self.get_open_billing_period(account_id)
        account = self._get_user_account_by_id(account_id)
        balance = self._account_balance(account_id)
        self.apply_withdraw_transaction(account_id=account.id, transaction_type=TransactionTypes.PAYMENT, description="Payoff", amount=balance)
        bp.updated_at = datetime.now()
        bp.end_date = datetime.now()
        self._update_account_balance(account_id, 0)
        self._create_billing_period(account_id)

        return balance

    def _create_billing_period(self, account_id: str) -> BillingPeriod:
        billing_period = BillingPeriod(
            id=str(len(self.storage["billing_periods"]) + 1),
            account_id=account_id,
            start_date=datetime.now(),
            end_date=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.storage["billing_periods"].append(billing_period)
        return billing_period

@lru_cache()
def get_account_repo():
    return InMemoryAccountRepo()