from fastapi import FastAPI
from app.routers import evaluation
import uvicorn

app = FastAPI()

app.include_router(evaluation.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)