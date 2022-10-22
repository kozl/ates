import pytest
import asyncio
import pytest_asyncio
from tortoise.contrib.test import finalizer, initializer

from repos.accounts.orm import AccountORM, TransactionORM, BillingPeriodORM
from repos.tasks.orm import TaskORM


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function", autouse=True)
async def init_orm(event_loop):
    initializer(["repos.tasks.orm", "repos.accounts.orm"], "sqlite://:memory:", app_label="models", loop=event_loop)
    initial_accounts = [
        AccountORM(username="ivan", balance=0),
    ]
    initial_billing_periods = [
        BillingPeriodORM(account_id=1, start_date="2020-01-01", end_date=None),
    ]
    initial_tranasactions = [
        TransactionORM(account_id=1, billing_period_id=1, type="TASK_ASSIGNED", debit=10, credit=0),
        TransactionORM(account_id=1, billing_period_id=1, type="TASK_COMPLETED", debit=0, credit=20),
    ]
    for acc in initial_accounts:
        await acc.save()

    for bp in initial_billing_periods:
        await bp.save()

    for tr in initial_tranasactions:
        await tr.save()

    yield
    finalizer()