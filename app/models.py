from sqlalchemy import Column, Integer, String, ForeignKey, Enum, JSON, DateTime, Text, Table
from sqlalchemy.orm import declarative_base, relationship, backref
import enum
from datetime import datetime

Base = declarative_base()

class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"


project_members = Table(
    "project_members",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
    Column("role", String(50), default="member", nullable=False)
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String(100), index=True, nullable=False)
    email = Column(String(100), nullable=False, index=True, unique=True)
    hashed_password = Column(String(255), nullable=False)
    
    projects = relationship("Project", secondary=project_members, back_populates="members")
    
class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String(150), nullable=False)
    description = Column(String(150), nullable=True)
    
    members = relationship("User", secondary=project_members, back_populates="projects")
    sources = relationship("Source", back_populates="project", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    milestones = relationship("Milestone", back_populates="project", cascade="all, delete-orphan")

class Source(Base):
    __tablename__ = "sources"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), index=True, nullable=False)
    source_type = Column(String(100), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    project = relationship("Project", back_populates="sources")
    raw_logs = relationship("RawIngestionLog", back_populates="source", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="source")
    
class RawIngestionLog(Base):
    __tablename__ = "raw_ingestion_logs"
    
    id = Column(Integer, primary_key=True, nullable=False)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    payload = Column(Text)
    status = Column(String)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    source = relationship("Source", back_populates="raw_logs")
    
class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), index=True, nullable=False)
    email = Column(String(100), nullable=True, index=True)
    phone = Column(String(100), nullable=True)
    custom_fields = Column(JSON, default=dict)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)
    
    project = relationship("Project", back_populates="leads")
    source = relationship("Source", back_populates="leads")
    tasks = relationship("Task", back_populates="lead")
    
class Milestone(Base):
    __tablename__ = "milestones"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100), index=True, nullable=False)
    due_date = Column(DateTime, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    project = relationship("Project", back_populates="milestones")
    tasks = relationship("Task", back_populates="milestone")
    
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100), index=True, nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    milestone_id = Column(Integer, ForeignKey("milestones.id"), nullable=True)
    parent_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    
    subtasks = relationship("Task", backref=backref("parent", remote_side=[id]))
    project = relationship("Project", back_populates="tasks")
    lead = relationship("Lead", back_populates="tasks")
    milestone = relationship("Milestone", back_populates="tasks")
    