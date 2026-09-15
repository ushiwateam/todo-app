from fastapi import FastAPI

from app.auth.presentation.router import router as auth_router
from app.todos.presentation.router import router as todos_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(todos_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
