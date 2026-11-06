from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Project, User
from app.schemas import ProjectCreate, ProjectResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_project = Project(**project.model_dump(), owner_id=current_user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/", response_model=list[ProjectResponse])
def get_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Project).filter(Project.owner_id == current_user.id).all()

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session=Depends(get_db), current_user: User = Depends(get_current_user)):
    result = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    
    if(result):
        return result
    
    raise HTTPException(status_code=404, detail="Project is not found")
