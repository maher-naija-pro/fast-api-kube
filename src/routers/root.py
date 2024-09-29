from fastapi import APIRouter, Request
from prometheus_client import Counter,Histogram, generate_latest
from fastapi.responses import PlainTextResponse
from helpers.log.logger import init_log
from time import time
import os 

router = APIRouter()

# init logger
logger=init_log()

# Define Prometheus root
REQUEST_COUNTER_ROOT = Counter('root_app_requests_total', 'Total number of requests of endpoint root')
ERROR_COUNTER_ROOT = Counter('root_app_request_errors_total', 'Total number of request errors of endpoint root')
REQUEST_LATENCY_ROOT = Histogram('root_app_request_latency_seconds', 'Request latency in seconds of endpoint root')

@router.get("/")
async def root(request: Request):
    start_time = time()

    logger.info(f"Root / requested from {request.client.host}")

    is_k8s = "KUBERNETES_SERVICE_HOST" in os.environ
    return {
        "version": "0.1.0",
        "date": int(time()),
        "kubernetes": is_k8s
    }
    # Measure request latency
    duration = time() - start_time
    REQUEST_LATENCY_ROOT.observe(duration)
    REQUEST_COUNTER_ROOT.inc()

    logger.info(f"Request completed in {duration:.4f} seconds")


