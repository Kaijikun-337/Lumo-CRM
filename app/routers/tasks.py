from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Milestone, Project, Task, User
from app.schemas import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = (
        db.query(Project)
        .filter(Project.id == task.project_id, Project.owner_id == current_user.id)
        .first()
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {task.project_id} not found",
        )

    if task.milestone_id is not None:
        milestone = (
            db.query(Milestone)
            .join(Project)
            .filter(Milestone.id == task.milestone_id, Project.owner_id == current_user.id)
            .first()
        )
        if not milestone:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Milestone with ID {task.milestone_id} not found",
            )

    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    project_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Task).join(Project).filter(Project.owner_id == current_user.id)
    if project_id is not None:
        query = query.filter(Task.project_id == project_id)
    return query.all()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = (
        db.query(Task)
        .join(Project)
        .filter(Task.id == task_id, Project.owner_id == current_user.id)
        .first()
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return result