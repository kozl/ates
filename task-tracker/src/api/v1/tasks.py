from typing import List

from fastapi import APIRouter, Header, Depends, HTTPException, status

from api.v1.models import Task, CreateTaskRequest, Result, Ok
from services.task_tracker import TaskTrackerService, get_service
from services.task_tracker import (
    UserNotFoundException, 
    TaskNotFoundException, 
    NoUsersFoundException, 
    UserIsNotAssigneeException,
)

router = APIRouter()

@router.get("/", response_model=Result)
async def list_tasks(
    x_user: str = Header(), 
    service: TaskTrackerService = Depends(get_service),
    ) -> Result:
    try:
        tasks = service.list_tasks(x_user)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    tasks = [Task(id=task.id, description=task.description, status=task.status.value, assignee=task.assignee) for task in tasks]

    return Result(result=tasks)

@router.post("/", response_model=Result)
async def create_task(
    request: CreateTaskRequest,
    service: TaskTrackerService = Depends(get_service)
    ) -> Result:
    try:
        task = service.create_task(request.description)
    except NoUsersFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return Result(result=Task(id=task.id, description=task.description, status=task.status.value, assignee=task.assignee))

@router.get("/{task_id}", response_model=Result)
async def get_task(task_id: str, service: TaskTrackerService = Depends(get_service)):
    try:
        task = service.get_task(task_id)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return Result(result=Task(id=task.id, description=task.description, status=task.status.value, assignee=task.assignee))

@router.post("/{task_id}/close", response_model=Result)
async def close_task(task_id: str, x_user: str = Header(default=None), service: TaskTrackerService = Depends(get_service)):
    try:
        task = service.close_task(task_id, x_user)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserIsNotAssigneeException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    return Result(result=Task(id=task.id, description=task.description, status=task.status.value, assignee=task.assignee))


@router.post("/assign", response_model=Result)
async def assign_all_tasks(x_user: str = Header(default=None), service: TaskTrackerService = Depends(get_service)):
    service.assign_all_tasks()
    return Result(result=Ok(ok=True))