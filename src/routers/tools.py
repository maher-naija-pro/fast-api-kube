import sys
sys.path = ["", ".."] + sys.path[1:]
sys.path.append("src")
from prometheus_client import Counter, Histogram

from src.models.log import QueryLog
from fastapi import APIRouter,Request,HTTPException,Depends
from pydantic import BaseModel
from db.database import get_db
from helpers.log.logger import init_log
from sqlalchemy.orm import Session
from db.database import get_db
from pydantic import BaseModel
import ipaddr
import socket
from time import time
import ipaddress
# API router with prefix '/tools'
router= APIRouter(prefix='/tools')
# Initialize logger for logging application events and errors
logger=init_log()

class IPSchema(BaseModel):
    ip: str


# Helper function to log successful domain queries
def log_query( domain: str,  ipv4s: list,db: Session= Depends(get_db)):
    query_log = QueryLog(domain=domain,client_ip=ipv4s)
    db.add(query_log)
    db.commit()

# Define Prometheus metrics
REQUEST_COUNTER_VALIDATE = Counter('validate_app_requests_total', 'Total number of requests on validate endpoint')
VALIDATE_DURATION = Histogram('validate_request_duration_seconds', 'Duration of /validate requests')
@router.post("/validate")
def validate_ip(request: Request, ip_data: IPSchema):
    start_time = time()  # Track the start time for measuring request duration
    REQUEST_COUNTER_VALIDATE.inc()  # Increment Prometheus counter for /validate endpoint
    client_ip = request.client.host  # Capture the client's IP address

    logger.info(f"Validating IP from {client_ip}: {ip_data.ip}")  # Log validation attempt

    try:
        # Use ipaddress library for enhanced validation (supports both IPv4 and IPv6)
        ip = ip_data.ip
        ip_obj = ipaddress.ip_address(ip)
        is_valid = ip_obj.version == 4  # Check if the IP is IPv4
        logger.info(f"IP {ip} is valid: {is_valid}")  # Log the result of the validation
        return {"ip": ip, "valid": is_valid}  # Return the result in a JSON response
    except ValueError as e:
        # If the IP is invalid, log the error and return a 400 Bad Request response
        logger.error(f"Invalid IP address provided by {client_ip}: {ip}")
        raise HTTPException(status_code=400, detail="Invalid IP address")
    finally:
        # Record the time taken for the /validate request in the Prometheus histogram
        VALIDATE_DURATION.observe(time() - start_time)




LOOKUP_DURATION = Histogram('lookup_request_duration_seconds', 'Duration of /lookup requests')
REQUEST_COUNTER_LOOKUP = Counter('lookup_app_requests_total', 'Total number of requests on lookup endpoint')
@router.get("/lookup")
def lookup(domain: str, request: Request, db: Session = Depends(get_db)):
    start_time = time()  # Track the start time for measuring request duration
    REQUEST_COUNTER_LOOKUP.inc()  # Increment Prometheus counter for /lookup endpoint
    client_ip = request.client.host  # Capture the client's IP address
    logger.info(f"Lookup request from {client_ip} for domain: {domain}")  # Log lookup attempt


    try:
        # Resolve the domain to get only IPv4 addresses
        ipv4s = socket.gethostbyname_ex(domain)[2] 
        # Log the successful domain query in the database
        log_query( domain, ipv4s, db )  # Save query in the database
        logger.info(f"Lookup success for domain {domain} by {client_ip}: {ipv4s}")  # Log lookup success
        return {"domain": domain, "ipv4": ipv4s}  # Return the resolved IPv4 addresses
    except socket.gaierror:
        # If the domain is not found, log the error and return a 400 Bad Request response
        logger.error(f"Domain lookup failed for {domain} from {client_ip}")
        raise HTTPException(status_code=400, detail="Domain not found")
    finally:
        # Record the time taken for the /lookup request in the Prometheus histogram
        LOOKUP_DURATION.observe(time() - start_time)

