from fastapi.testclient import TestClient

from app import app
from repos.tasks.orm import get_task_repo
from repos.accounts.orm import get_account_repo
from tests.functional.mocks.tasks_repo import get_task_repo as get_mock_task_repo
from tests.functional.mocks.accounts_repo import get_account_repo as get_mock_account_repo
from tests.functional.fixtures.orm import init_orm


# app.dependency_overrides[get_task_repo] = get_mock_task_repo
# app.dependency_overrides[get_account_repo] = get_mock_account_repo

def test_list_accounts(init_orm):
    with TestClient(app) as client:
        response = client.get("/v1/accounts", headers={"X-User": "ivan", "X-Role": "developer"})
        assert response.status_code == 200
        data = response.json()
        assert len(data['result']) == 1

def test_list_my_account(init_orm):
    with TestClient(app) as client:
        response = client.get("/v1/accounts/my", headers={"X-User": "ivan", "X-Role": "developer"})
        assert response.status_code == 200
        data = response.json()
        assert data['result']['user_id'] == "ivan"
        assert data['result']['balance'] == -100
        assert len(data['result']['transactions']) == 3

        response = client.get("/v1/accounts/my", headers={"X-User": "ivan2", "X-Role": "developer"})
        assert response.status_code == 404