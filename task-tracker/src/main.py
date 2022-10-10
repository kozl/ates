import logging
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
import uvicorn as uvicorn

from api.v1 import tasks
from core.config import SERVICE_NAME, USER_HEADER, ROLE_HEADER
from core.logger import LOGGING

app = FastAPI(
    title=SERVICE_NAME,
    openapi_url="/api/openapi.json",
)

app.include_router(tasks.router, prefix='/v1/tasks', tags=['tasks'])

@app.middleware("http")
async def ensure_headers(request: Request, call_next):
    x_user = request.headers.get(USER_HEADER)
    if x_user is None or x_user == "":
        return Response(status_code=400, content=f"{USER_HEADER} header is required")

    x_role = request.headers.get(ROLE_HEADER)
    if x_role is None or x_role == "":
        return Response(status_code=400, content=f"{ROLE_HEADER} header is required")
    return await call_next(request)

@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"reason": exc.detail}},
    )

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )