from fastapi import FastAPI

from src.routing import router as core_router

app = FastAPI()

app.include_router(core_router)
