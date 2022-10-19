from fastapi.testclient import TestClient

from app import app
from repos.tasks.orm import get_task_repo
from repos.users.orm import get_user_repo
from tests.functional.mocks.task_repo import get_task_repo as get_mock_task_repo
from tests.functional.mocks.user_repo import get_user_repo as get_mock_user_repo

client = TestClient(app)

app.dependency_overrides[get_task_repo] = get_mock_task_repo
app.dependency_overrides[get_user_repo] = get_mock_user_repo

def test_list_tasks():
    response = client.get("/v1/tasks", headers={"X-User": "developer1", "X-Role": "developer"})
    assert response.status_code == 200
    data = response.json()
    assert len(data['result']) == 1
    
def test_show_task():
    response = client.get("/v1/tasks/POPUG-1", headers={"X-User": "developer1", "X-Role": "developer"})
    assert response.status_code == 200

def test_create_task():
    response = client.post(
        "/v1/tasks", 
        headers={"X-User": "developer1", "X-Role": "developer"}, 
        json={"title": "New task", "description": "New task"})
    assert response.status_code == 200
    data = response.json()
    assert data['result']['id'] == 'POPUG-5'

def test_close_task():
    response = client.post(
        "/v1/tasks/POPUG-4/close", 
        headers={"X-User": "accountant", "X-Role": "accountant"})
    assert response.status_code == 200
    data = response.json()
    assert data['result']['status'] == 'closed'

    response = client.get("/v1/tasks/POPUG-4", headers={"X-User": "accountant", "X-Role": "accountant"})
    assert response.status_code == 200
    data = response.json()
    assert data['result']['status'] == 'closed'

def test_assign_tasks():
    response = client.post(
        "/v1/tasks/assign", 
        headers={"X-User": "accountant", "X-Role": "accountant"})
    assert response.status_code == 200