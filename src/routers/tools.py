"""
Tools endpoints for IP validation and domain lookup.

This module defines two tools endpoints: one for validating IP addresses
and anotherfor looking up domain names and resolving them to IPv4 addresses.
 It integrates with Prometheus to track request metrics and logs activity
 for debugging purposes.

Classes:
    IPSchema: Pydantic model representing an IP address for validation.

Functions:
    log_query(domain, ipv4s, db): Helper function to log successful domain queries.
    validate_ip(request, ip_data): Validates if the given IP address is a valid
IPv4 address.
    lookup(domain, request, db): Looks up a domain name and resolves it to its
    IPv4 addresses.

Metrics:
    REQUEST_COUNTER_VALIDATE: A counter for the total number of requests to the
    /validate endpoint.
    VALIDATE_DURATION: A histogram tracking the duration of /validate requests.
    REQUEST_COUNTER_LOOKUP: A counter for the total number of requests to the
    /lookup endpoint.
    LOOKUP_DURATION: A histogram tracking the duration of /lookup requests.

Routes:
    /tools/validate: A POST endpoint for IP address validation.
    /tools/lookup: A GET endpoint for domain lookup.
"""

import ipaddress
import socket
import sys
from time import time

from fastapi import APIRouter, Depends, HTTPException, Request
from prometheus_client import Counter, Histogram
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.database import get_db
from helpers.log.logger import init_log
from src.models.log import QueryLog

sys.path = ["", ".."] + sys.path[1:]
sys.path.append("src")

# API router with prefix '/tools'
router = APIRouter(prefix="/tools")
# Initialize logger for logging application events and errors
logger = init_log()


class IPSchema(BaseModel):
    """
    Pydantic model for IP validation requests.

    Attributes:
        ip (str): The IP address to be validated.
    """

    ip: str


# Helper function to log successful domain queries
def log_query(domain: str, ipv4s: list, db: Session = Depends(get_db)):
    """
    Logs successful domain lookup queries in the database.

    Args:
        domain (str): The domain name queried.
        ipv4s (list): A list of IPv4 addresses resolved from the domain.
        db (Session): Database session to store the query log.
    """
    query_log = QueryLog(domain=domain, client_ip=ipv4s)
    db.add(query_log)
    db.commit()


# Define Prometheus metrics
REQUEST_COUNTER_VALIDATE = Counter(
    "validate_app_requests_total", "Total number of req on validate endpoint"
)
VALIDATE_DURATION = Histogram(
    "validate_request_duration_seconds", "Duration of /validate requests"
)


@router.post("/validate")
def validate_ip(request: Request, ip_data: IPSchema):
    """
    Validates the given IP address.

    Args:
        request (Request): The incoming HTTP request object.
        ip_data (IPSchema): The IP data sent in the request.

    Returns:
        dict: A dictionary indicating if the IP is valid.

    Raises:
        HTTPException: If the IP address is invalid.
    """
    start_time = time()  # Track the start time for measuring request duration
    REQUEST_COUNTER_VALIDATE.inc()  # Increment Prometheus counter for /validate
    client_ip = request.client.host  # Capture the client's IP address

    logger.info(
        f"Validating IP from {client_ip}: {ip_data.ip}"
    )  # Log validation attempt

    try:
        # Use ipaddress library for enhanced validation (supports both IPv4 and IPv6)
        ip = ip_data.ip
        ip_obj = ipaddress.ip_address(ip)
        is_valid = ip_obj.version == 4  # Check if the IP is IPv4
        logger.info(f"IP {ip} is valid: {is_valid}")  # Log the result of the validation
        return {"ip": ip, "valid": is_valid}  # Return the result in a JSON response
    except Exception as e:
        # If the IP is invalid, log the error and return a 400 Bad Request response
        logger.error(f"Invalid IP address provided by {client_ip}: {ip}  {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid IP address") from e
    finally:
        # Record the time taken for the /validate request in the Prometheus histogram
        VALIDATE_DURATION.observe(time() - start_time)


LOOKUP_DURATION = Histogram(
    "lookup_request_duration_seconds", "Duration of /lookup requests"
)
REQUEST_COUNTER_LOOKUP = Counter(
    "lookup_app_requests_total", "Total number of requests on lookup endpoint"
)


@router.get("/lookup")
def lookup(domain: str, request: Request, db: Session = Depends(get_db)):
    """
    Performs a domain lookup to resolve IPv4 addresses.

    Args:
        domain (str): The domain name to resolve.
        request (Request): The incoming HTTP request object.
        db (Session): Database session to log the domain query.

    Returns:
        dict: A dictionary with the domain and resolved IPv4 addresses.

    Raises:
        HTTPException: If the domain name could not be resolved.
    """
    start_time = time()  # Track the start time for measuring request duration
    REQUEST_COUNTER_LOOKUP.inc()  # Increment Prometheus counter for /lookup
    client_ip = request.client.host  # Capture the client's IP address
    logger.info(
        f"Lookup request from {client_ip} for domain: {domain}"
    )  # Log lookup attempt

    try:
        # Resolve the domain to get only IPv4 addresses
        ipv4s = socket.gethostbyname_ex(domain)[2]
        # Log the successful domain query in the database
        log_query(domain, ipv4s, db)  # Save query in the database
        logger.info(
            f"Lookup success for domain {domain} by {client_ip}: {ipv4s}"
        )  # Log lookup success
        return {"domain": domain, "ipv4": ipv4s}  # Return the resolved IPv4 addresses
    except socket.gaierror:
        # If domain not found, log the error and return 400 Bad Request response
        logger.error(f"Domain lookup failed for {domain} from {client_ip}")
        raise HTTPException(
            status_code=400, detail="Domain not found"
        ) from socket.gaierror
    finally:
        # Record the time taken for the /lookup request in the Prometheus histogram
        LOOKUP_DURATION.observe(time() - start_time)
