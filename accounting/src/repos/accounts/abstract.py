from abc import ABC, abstractmethod
from typing import List

from repos.accounts.models import Account, BillingPeriod, Transaction, BillingPeriod, TransactionTypes

class AccountsRepo(ABC):

    @abstractmethod
    def get_user_account(self, username: str) -> Account:
        pass

    @abstractmethod
    def list_accounts(self) -> List[Account]:
        pass

    @abstractmethod
    def add_user_account(self, username: str) -> Account:
        pass

    @abstractmethod
    def apply_withdraw_transaction(self, account_id: str, transaction_type: TransactionTypes, amount: int) -> Transaction:
        pass

    @abstractmethod
    def apply_debit_transaction(self, account_id: str, transaction_type: TransactionTypes, amount: int) -> Transaction:
        pass

    @abstractmethod
    def list_account_transactions(self, account_id: str, open_billing_period: bool = True) -> List[Transaction]:
        pass

    @abstractmethod
    def get_open_billing_period(self, account_id: str) -> BillingPeriod:
        pass

    @abstractmethod
    def close_billing_period(self, account_id: str) -> int:
        pass