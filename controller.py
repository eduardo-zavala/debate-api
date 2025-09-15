from fastapi import APIRouter, HTTPException
from models import DebateRequest, DebateResponse
from service import debate_service

router = APIRouter(prefix="", tags=["debate"])

@router.post("/debate")
def debate(request: DebateRequest) -> DebateResponse:
    try:
        response = debate_service.process_debate(request)
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))