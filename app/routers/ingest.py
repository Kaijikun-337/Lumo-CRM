import json
from typing import Any
from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Source, RawIngestionLog
from app.schemas import BaseResponseSchema
from app.services.ingestion import process_raw_ingestion_log
from app.dependencies import get_current_user
from app.models import Project, User

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

class IngestionAckResponse(BaseResponseSchema):
    message: str
    log_id: int
    status: str


@router.post(
    "/{source_id}",
    response_model=IngestionAckResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def ingest_lead(
    source_id: int,
    background_tasks: BackgroundTasks,
    payload: dict[str, Any] = Body(
        ...,
        example={
            "full_name": "Elena Rostova",
            "email": "elena@example.com",
            "phone": "+43 1 234 5678",
            "company": "Tech Austria",
            "estimated_budget": 12000,
        },
    ),
    db: Session = Depends(get_db),
):
    # 1. Verify source exists
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source with ID {source_id} not found",
        )

    # 2. Persist raw payload immediately to raw_ingestion_logs
    raw_payload_str = json.dumps(payload) if isinstance(payload, (dict, list)) else str(payload)
    
    log_entry = RawIngestionLog(
        source_id=source.id,
        payload=raw_payload_str,
        status="PENDING",
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)

    # 3. Offload normalization & lead creation to BackgroundTasks
    background_tasks.add_task(process_raw_ingestion_log, log_entry.id)

    # 4. Instant asynchronous response
    return IngestionAckResponse(
        message="Payload accepted for processing",
        log_id=log_entry.id,
        status="PENDING",
    )

@router.get("/logs", status_code=status.HTTP_200_OK)
def get_ingestion_logs(
    source_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        db.query(RawIngestionLog)
        .join(Source)
        .join(Project)
        .filter(Project.owner_id == current_user.id)
    )
    if source_id is not None:
        query = query.filter(RawIngestionLog.source_id == source_id)
    return query.order_by(RawIngestionLog.created_at.desc()).all()