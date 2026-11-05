from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Source, Lead
from app.schemas import LeadResponse
from app.parsers.factory import ParserFactory

router = APIRouter(prefix="/ingest", tags=["Ingestion"])


@router.post("/{source_id}", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def ingest_lead(
    source_id: int,
    payload: dict[str, Any] = Body(
        ...,
        example={
            "full_name": "Elena Rostova",
            "email": "elena@example.com",
            "phone": "+43 1 234 5678",
            "company": "Tech Austria",
            "estimated_budget": 12000
        }
    ),
    db: Session = Depends(get_db)
):
    # 1. Verify source exists in SQLite
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source with ID {source_id} not found"
        )

    # 2. Resolve parser instance and normalize incoming payload dictionary
    parser = ParserFactory.get_parser(source.source_type)
    normalized_data = parser.parse(payload)

    # 3. Save normalized Lead to database
    db_lead = Lead(
        name=normalized_data["name"],
        email=normalized_data["email"],
        phone=normalized_data["phone"],
        custom_fields=normalized_data["custom_fields"],
        project_id=source.project_id,
        source_id=source.id,
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead