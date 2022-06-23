from uuid import UUID

from fastapi import FastAPI

from dotenv import load_dotenv

import services.AppService as AppService
from models.QuestDbDeployment import QuestDbDeployment

load_dotenv()

app = FastAPI()


@app.post("/")
async def create_deployment():
    return await AppService.create()


@app.get("/{deployment_id}", response_model=QuestDbDeployment)
async def get_deployment(deployment_id: str):
    return await AppService.get(UUID(deployment_id))


@app.delete("/{deployment_id}", response_model=QuestDbDeployment)
async def delete_deployment(deployment_id: str):
    return await AppService.delete(UUID(deployment_id))
