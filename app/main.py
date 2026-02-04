from fastapi import FastAPI

from app.routers import auth, user, task

app = FastAPI(title="Task Management System")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(task.router)

@app.get("/")
def home():
    return {"message": "Welcome to Task Management System"}

@app.get("/health")
def health_check():
    return { "message" : "Task Management System is running!"}