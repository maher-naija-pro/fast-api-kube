from fastapi import APIRouter
from prometheus_client import Counter, generate_latest
from fastapi.responses import PlainTextResponse

router = APIRouter()

# Define Prometheus metrics
REQUEST_COUNTER = Counter('app_requests_total', 'Total number of requests')

@router.get("/metrics", response_class=PlainTextResponse)
def metrics():
    REQUEST_COUNTER.inc()  # Increment the counter for each request
    return generate_latest()