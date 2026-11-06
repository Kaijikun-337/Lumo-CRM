from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models import TaskStatus

class BaseResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    
class ProjectResponse(BaseResponseSchema):
    id: int
    name: str
    description: str | None = None
    
class SourceCreate(BaseModel):
    name: str
    source_type: str
    project_id: int 
    
class SourceResponse(BaseResponseSchema):
    id: int
    name: str
    source_type: str
    project_id: int
    
class LeadCreate(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    custom_fields: dict | None = None
    project_id: int
    source_id: int | None = None
    
class LeadResponse(BaseResponseSchema):
    id: int    
    name: str
    email: str | None = None
    phone: str | None = None
    custom_fields: dict | None = None
    project_id: int
    source_id: int | None = None
    
class MilestoneCreate(BaseModel):
    title: str
    due_date: datetime | None = None
    project_id: int

class MilestoneResponse(BaseResponseSchema):
    id: int
    title: str
    due_date: datetime | None = None
    project_id: int

class TaskCreate(BaseModel):
    title: str
    notes: str | None = None
    status: TaskStatus = TaskStatus.TODO
    project_id: int
    lead_id: int | None = None
    milestone_id: int | None = None
    parent_id: int | None = None
    
class TaskResponse(BaseResponseSchema):
    id: int
    title: str
    notes: str | None = None
    status: TaskStatus = TaskStatus.TODO
    project_id: int
    lead_id: int | None = None
    milestone_id: int | None = None
    parent_id: int | None = None

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseResponseSchema):
    id: int
    name: str
    email: str
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"