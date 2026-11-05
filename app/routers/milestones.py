from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Milestone, Project
from app.schemas import MilestoneCreate, MilestoneResponse

router = APIRouter(prefix="/milestones", tags=["Milestones"])

@router.post("/", response_model=MilestoneResponse, status_code=status.HTTP_201_CREATED)
def create_milestone(milestone: MilestoneCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == milestone.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {milestone.project_id} not found"
        )    
    
    db_milestone = Milestone(**milestone.model_dump())
    db.add(db_milestone)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone

@router.get("/", response_model=list[MilestoneResponse])
def get_milestones(db:Session = Depends(get_db)):
    return db.query(Milestone).all()
    
@router.get("/{milestone_id}", response_model=MilestoneResponse)
def get_milestone(milestone_id: int, db: Session = Depends(get_db)):
    result = db.query(Milestone).filter(Milestone.id == milestone_id).first()
    
    if(result):
        return result
    
    raise HTTPException(status_code=404, detail="Milestone is not found")