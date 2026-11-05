from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Lead, Project, Source
from app.schemas import LeadCreate, LeadResponse

router = APIRouter(prefix="/leads", tags=["Leads"])

@router.post("/", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def create_lead(lead:LeadCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == lead.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {lead.project_id} not found"
        )
        
    if lead.source_id is not None:
        source = db.query(Source).filter(Source.id == lead.source_id).first()
        if not source:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Source with ID {lead.source_id} not found"
            )
    db_lead = Lead(**lead.model_dump())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

@router.get("/", response_model=list[LeadResponse])
def get_leads(project_id: int | None = None, db: Session = Depends(get_db)):
    if(project_id):
        return db.query(Lead).filter(Lead.project_id == project_id)
    return db.query(Lead).all()

@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    result = db.query(Lead).filter(Lead.id == lead_id).first()
    
    if(result):
        return result
    
    raise HTTPException(status_code=404, detail="Lead is not found")
    