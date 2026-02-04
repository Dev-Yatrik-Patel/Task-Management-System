from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError

from app.core.responses import error_response
from app.routers import auth, user, task

app = FastAPI(title="Task Management System")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(task.router)

@app.exception_handler(HTTPException)
async def app_exception_handler(request: Request, exc: HTTPException):
    return error_response(
        message=exc.detail,
        error_code="HTTP_ERROR",
        status_code=exc.status_code
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return error_response(
        message="Validation error",
        error_code="VALIDATION_ERROR",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        details=str(exc.errors())
    )

@app.get("/")
def home():
    return {"message": "Welcome to Task Management System"}

@app.get("/health")
def health_check():
    return { "message" : "Task Management System is running!"}