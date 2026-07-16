from fastapi import FastAPI
from app.api.routers.auth import router as auth_router
from app.api.routers.todos import router as todos_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(todos_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}