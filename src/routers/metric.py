from fastapi import APIRouter, Request
from prometheus_client import Counter,Histogram, generate_latest
from fastapi.responses import PlainTextResponse
from helpers.log.logger import init_log
from time import time

router = APIRouter()

# init logger
logger=init_log()

# Define Prometheus metrics
REQUEST_COUNTER_METRICS = Counter('metric_app_requests_total', 'Total number of requests of endpoint metrics')
ERROR_COUNTER_METRICS = Counter('metric_app_request_errors_total', 'Total number of request errors of endpoint metrics')
REQUEST_LATENCY_METRICS = Histogram('metric_app_request_latency_seconds', 'Request latency in seconds of endpoint metrics')

@router.get("/metrics", response_class=PlainTextResponse)
def metrics(request: Request):
    start_time = time()  # Track the start time for latency measurement
    REQUEST_COUNTER_METRICS.inc()  # Increment the counter for each request
    try:
        # Log request data for debugging
        logger.debug(f"Request to /metrics from {request.client.host}")

        # Generate Prometheus metrics data
        metrics_data = generate_latest()

        # Log success with latency
        request_latency = time() - start_time
        REQUEST_LATENCY_METRICS.observe(request_latency)
        logger.info(f"Metrics served in {request_latency:.4f} seconds")

        return PlainTextResponse(metrics_data, media_type="text/plain")

    except Exception as e:
        # Log the error and increment error counter
        ERROR_COUNTER_METRICS.inc()
        logger.error(f"Error serving /metrics: {str(e)}")
        raise PlainTextResponse(f"Internal server error: {str(e)}", status_code=500)










