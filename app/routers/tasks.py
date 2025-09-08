from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from app import models, schemas, utils, database

router = APIRouter(prefix="/tasks", tags=["tasks"])
get_db = database.get_db
get_current_user = utils.get_current_user


@router.post("/", response_model=schemas.TaskOut)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_task = models.Task(**task.model_dump(), owner_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/", response_model=List[schemas.TaskOut])
def list_tasks(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    tasks = db.scalars(
        select(models.Task).filter(models.Task.owner_id == current_user.id)
    ).all()
    return tasks


@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_task = db.scalar(
        select(models.Task).filter(
            models.Task.id == task_id, models.Task.owner_id == current_user.id
        )
    )
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_task = db.scalar(
        select(models.Task).filter(
            models.Task.id == task_id, models.Task.owner_id == current_user.id
        )
    )
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted"}


@router.get("/stats", response_model=schemas.TaskStats)
def get_task_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    tasks = db.scalars(
        select(models.Task).filter(models.Task.owner_id == current_user.id)
    ).all()

    total = len(tasks)
    completed = len([t for t in tasks if t.completed])
    pending = total - completed

    priority: dict[int, int] = {}
    for t in tasks:
        priority[t.priority] = priority.get(t.priority, 0) + 1

    return schemas.TaskStats(
        total=total,
        completed=completed,
        pending=pending,
        priority=priority,
    )
