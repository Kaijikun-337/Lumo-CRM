from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Milestone, Project, User
from app.schemas import MilestoneCreate, MilestoneResponse

router = APIRouter(prefix="/milestones", tags=["Milestones"])


@router.post("/", response_model=MilestoneResponse, status_code=status.HTTP_201_CREATED)
def create_milestone(
    milestone: MilestoneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = (
        db.query(Project)
        .filter(Project.id == milestone.project_id, Project.owner_id == current_user.id)
        .first()
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {milestone.project_id} not found",
        )

    db_milestone = Milestone(**milestone.model_dump())
    db.add(db_milestone)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone


@router.get("/", response_model=list[MilestoneResponse])
def get_milestones(
    project_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Milestone).join(Project).filter(Project.owner_id == current_user.id)
    if project_id is not None:
        query = query.filter(Milestone.project_id == project_id)
    return query.all()


@router.get("/{milestone_id}", response_model=MilestoneResponse)
def get_milestone(
    milestone_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = (
        db.query(Milestone)
        .join(Project)
        .filter(Milestone.id == milestone_id, Project.owner_id == current_user.id)
        .first()
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Milestone with ID {milestone_id} not found",
        )
    return result