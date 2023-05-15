from datetime import datetime

from pytest import fixture

from repos.accounts.memory import InMemoryAccountRepo
from repos.accounts.models import Account, Transaction, BillingPeriod, TransactionTypes

@fixture
def inmemory_account_repo():
    return InMemoryAccountRepo(
        initial_accounts=[
            Account(id="1", username="user1", balance=0, created_at=datetime.now(), updated_at=datetime.now()),
        ],
        initial_transactions=[
            Transaction(id="1", account_id="1", billing_period_id="1", type=TransactionTypes.TASK_ASSIGNED.value, debit=100, credit=0, created_at=datetime.now()),
            Transaction(id="2", account_id="1", billing_period_id="1", type=TransactionTypes.TASK_COMPLETED.value, debit=0, credit=100, created_at=datetime.now()),
            Transaction(id="3", account_id="1", billing_period_id="1", type=TransactionTypes.TASK_COMPLETED.value, debit=0, credit=100, created_at=datetime.now()),
        ],
        initial_billing_periods=[
            BillingPeriod(id="1", account_id="1", start_date=datetime(2020, 1, 1), end_date=None, created_at=datetime.now(), updated_at=datetime.now()),
        ]
    )

def test_get_user_account(inmemory_account_repo):
    account = inmemory_account_repo.get_user_account("user1")
    assert account.id == "1"
    assert account.username == "user1"
    assert account.balance == -100

def test_apply_withdraw_or_debit_transactions(inmemory_account_repo):
    inmemory_account_repo.apply_deposit_transaction(account_id="1", transaction_type=TransactionTypes.TASK_COMPLETED, amount=100)
    account = inmemory_account_repo.get_user_account("user1")
    assert account.balance == 0

    inmemory_account_repo.apply_withdraw_transaction(account_id="1", transaction_type=TransactionTypes.TASK_ASSIGNED, amount=500)
    account = inmemory_account_repo.get_user_account("user1")
    assert account.balance == -500

def test_close_billing_period(inmemory_account_repo):
    balance = inmemory_account_repo.close_billing_period(account_id="1")
    assert balance == -100
    account = inmemory_account_repo.get_user_account("user1")
    assert account.balance == 0

    inmemory_account_repo.apply_deposit_transaction(account_id="1", transaction_type=TransactionTypes.TASK_COMPLETED, amount=100)
    account = inmemory_account_repo.get_user_account("user1")
    assert account.balance == 100