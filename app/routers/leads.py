from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Lead, Project, Source, User
from app.schemas import LeadCreate, LeadResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.post("/", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def create_lead(
    lead: LeadCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = (
        db.query(Project)
        .filter(Project.id == lead.project_id, Project.owner_id == current_user.id)
        .first()
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {lead.project_id} not found",
        )

    if lead.source_id is not None:
        source = (
            db.query(Source)
            .join(Project)
            .filter(Source.id == lead.source_id, Project.owner_id == current_user.id)
            .first()
        )
        if not source:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Source with ID {lead.source_id} not found",
            )

    db_lead = Lead(**lead.model_dump())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead


@router.get("/", response_model=list[LeadResponse])
def get_leads(
    project_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Lead).join(Project).filter(Project.owner_id == current_user.id)
    if project_id is not None:
        query = query.filter(Lead.project_id == project_id)
    return query.all()


@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = (
        db.query(Lead)
        .join(Project)
        .filter(Lead.id == lead_id, Project.owner_id == current_user.id)
        .first()
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lead with ID {lead_id} not found",
        )
    return result