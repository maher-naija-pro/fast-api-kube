from fastapi import APIRouter,Request,HTTPException 
from pydantic import BaseModel
import ipaddress

router= APIRouter(prefix='/tools')

class IPSchema(BaseModel):
    ip: str

@router.post("/validate")
def validate_ip(request: Request, ip: IPSchema):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return {"ip": ip, "valid": ip_obj.version == 4}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid IP address")
