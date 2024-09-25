import sys
sys.path = ["", ".."] + sys.path[1:]
sys.path.append("src")

from src.models.log import QueryLog
from fastapi import APIRouter,Request,HTTPException,Depends
from pydantic import BaseModel
from db.database import get_db
from helpers.log.logger import init_log
from sqlalchemy.orm import Session
from db.database import get_db
import ipaddr
import socket


router= APIRouter(prefix='/tools')
logger=init_log()

class IPSchema(BaseModel):
    ip: str

# Helper function to log successful domain queries
def log_query( domain: str,  ipv4s: list,db: Session= Depends(get_db)):
    query_log = QueryLog(domain=domain,client_ip=ipv4s)
    db.add(query_log)
    db.commit()


@router.post("/validate")
def validate_ip(request: Request, ip_data: IPSchema):
    try:
        ip = ip_data.ip
        print (ip)
        ip_obj = ipaddr.IPAddress(ip)
        print(ip_obj)
        return {"ip": ip, "valid": ip_obj.version == 4}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid IP address")

@router.get("/lookup")
def lookup(domain: str, db: Session = Depends(get_db)):
    try:
        ipv4s = socket.gethostbyname_ex(domain)[2]  # Get only IPv4 addresses
        log_query( domain, ipv4s, db )  # Save query in the database
        return {"domain": domain, "ipv4": ipv4s}
    except socket.gaierror:
        raise HTTPException(status_code=400, detail="Domain not found")