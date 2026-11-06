from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Source, Project, User
from app.schemas import SourceCreate, SourceResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/sources", tags=["Sources"])


@router.post("/", response_model=SourceResponse, status_code=status.HTTP_201_CREATED)
def create_source(
    source: SourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = (
        db.query(Project)
        .filter(Project.id == source.project_id, Project.owner_id == current_user.id)
        .first()
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {source.project_id} not found",
        )

    db_source = Source(**source.model_dump())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


@router.get("/", response_model=list[SourceResponse])
def get_sources(
    project_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Source).join(Project).filter(Project.owner_id == current_user.id)
    if project_id is not None:
        query = query.filter(Source.project_id == project_id)
    return query.all()


@router.get("/{source_id}", response_model=SourceResponse)
def get_source(
    source_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = (
        db.query(Source)
        .join(Project)
        .filter(Source.id == source_id, Project.owner_id == current_user.id)
        .first()
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source with ID {source_id} not found",
        )
    return result