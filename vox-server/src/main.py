from fastapi import FastAPI

from src.routes import heartbeat, vox

app = FastAPI()

app.include_router(
    heartbeat.router,
    prefix="/api/heartbeat",
    tags=["Root"],
)

app.include_router(
    vox.router,
    prefix="/api/vox",
    tags=["Root"],
)
