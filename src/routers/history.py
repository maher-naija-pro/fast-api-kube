from fastapi import APIRouter,Depends

from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from helpers.log.logger import init_log
from db.database import get_db
import sys
sys.path = ["", ".."] + sys.path[1:]
sys.path.append("src")

from src.models.log import QueryLog

router = APIRouter()
logger=init_log()


@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    logger.info("/history requested")
    history = db.query(QueryLog).order_by(QueryLog.created_time.desc()).limit(20).all()
    return history