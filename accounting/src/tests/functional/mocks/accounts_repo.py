from datetime import datetime
from functools import lru_cache

from repos.accounts.models import Account, Transaction, BillingPeriod, TransactionTypes
from repos.accounts.memory import InMemoryAccountRepo

@lru_cache()
def get_account_repo():
    return InMemoryAccountRepo(
        initial_accounts=[
            Account(id="1", username="ivan", balance=0, created_at=datetime.now(), updated_at=datetime.now()),
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