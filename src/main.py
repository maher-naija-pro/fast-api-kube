#!/usr/bin/python
import os 
import time
import sys
sys.path.append("routers")

from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import health
from routers import metric
from routers import tools

# Graceful shutdown logic

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    print("init lifespan")
    yield
    print("Shutting down gracefully...")
    
app = FastAPI(lifespan=app_lifespan)
app.include_router(health.router, prefix="")
app.include_router(metric.router, prefix="")
app.include_router(tools.router, prefix="/v1")


@app.get("/")
async def root():
    is_k8s = "KUBERNETES_SERVICE_HOST" in os.environ
    return {
        "version": "0.1.0",
        "date": int(time.time()),
        "kubernetes": is_k8s
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)