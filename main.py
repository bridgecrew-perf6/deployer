from uuid import UUID

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

import services.AppService as AppService
from services.StatusUpdateService import schedule_status_updates

load_dotenv()

app = FastAPI()


@app.post("/")
async def create_deployment():
    return await AppService.create()


@app.get("/{deployment_id}")
async def get_deployment(deployment_id: str):
    return await AppService.get(UUID(deployment_id))


@app.get("/{deployment_id}/status")
async def get_deployment(deployment_id: str):
    return await AppService.get_status(UUID(deployment_id))


@app.delete("/{deployment_id}")
async def delete_deployment(deployment_id: str):
    return await AppService.delete(UUID(deployment_id))


@app.on_event("startup")
@repeat_every(seconds=1)
async def update_scheduler():
    await schedule_status_updates()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
