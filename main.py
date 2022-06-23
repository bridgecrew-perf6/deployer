from uuid import UUID

from fastapi import FastAPI

from dotenv import load_dotenv

import services.AppService as AppService

import uvicorn

load_dotenv()

app = FastAPI()


@app.post("/")
async def create_deployment():
    return await AppService.create()


@app.get("/{deployment_id}")
async def get_deployment(deployment_id: str):
    return await AppService.get(UUID(deployment_id))


@app.delete("/{deployment_id}")
async def delete_deployment(deployment_id: str):
    return await AppService.delete(UUID(deployment_id))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
