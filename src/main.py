#!/usr/bin/python
import os 
import time
import sys
sys.path.append("routers")
sys.path.append("helpers")


from contextlib import asynccontextmanager
from fastapi import FastAPI

from helpers.log.logger import init_log
from db.database import get_db

from routers import health
from routers import metric
from routers import tools
from routers import history

db=get_db()

# Graceful shutdown logic
@asynccontextmanager
async def app_lifespan(app: FastAPI):
    logger.info("init lifespan")
    yield
    logger.info("Shutting down gracefully...")
    db.close()

logger=init_log()
logger.info('Hello start APP !!')



app = FastAPI(lifespan=app_lifespan)
app.include_router(health.router, prefix="")
app.include_router(metric.router, prefix="")
app.include_router(tools.router, prefix="/v1")
app.include_router(history.router, prefix="/v1")

@app.get("/")
async def root():
    logger.info(f"/ requested")
    is_k8s = "KUBERNETES_SERVICE_HOST" in os.environ
    return {
        "version": "0.1.0",
        "date": int(time.time()),
        "kubernetes": is_k8s
    }


#if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run(app, host="0.0.0.0", port=3000)