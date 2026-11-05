from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Source, Project
from app.schemas import SourceCreate, SourceResponse

router = APIRouter(prefix="/sources", tags=["Sources"])

@router.post("/", response_model=SourceResponse, status_code=status.HTTP_201_CREATED)
def create_source(source: SourceCreate, db: Session = Depends(get_db)):
    result = db.query(Project).filter(source.project_id == Project.id).first()
    
    if(result):
        db_source = Source(**source.model_dump())
        db.add(db_source)
        db.commit()
        db.refresh(db_source)
        return db_source
    
    raise HTTPException(status_code=404, detail="Project is not found")
    
@router.get("/", response_model=list[SourceResponse])
def get_sources(db: Session = Depends(get_db)):
    return db.query(Source).all()

@router.get("/{source_id}", response_model=SourceResponse)
def get_source(source_id: int, db: Session = Depends(get_db)):
    result = db.query(Source).filter(Source.id == source_id).first()
    
    if(result):
        return result
    
    raise HTTPException(status_code=404, detail="Source is not found")