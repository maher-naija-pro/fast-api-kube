#!/usr/bin/python
import os 
import time
import sys
sys.path.append("routers")

from fastapi import FastAPI
from routers import health
from routers import metric
from routers import tools

app = FastAPI()
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