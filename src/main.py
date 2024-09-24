#!/usr/bin/python
import os 
import time
import sys
sys.path.append("routers")

from fastapi import FastAPI
from routers import health
from routers import metric

app = FastAPI()
app.include_router(health.router, prefix="")
app.include_router(metric.router, prefix="")

@app.get("/")
async def root():
    is_k8s = "KUBERNETES_SERVICE_HOST" in os.environ
    return {
        "version": "0.1.0",
        "date": int(time.time()),
        "kubernetes": is_k8s
    }

