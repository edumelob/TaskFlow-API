"""
Rotas CRUD de tarefas. Todas as rotas exigem autenticação e cada usuário
só enxerga/manipula as próprias tarefas.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.auth import get_current_active_user
from app.database import get_db

router = APIRouter(prefix="/tasks", tags=["Tarefas"])


@router.get("/", response_model=List[schemas.TaskOut])
def list_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Lista as tarefas do usuário autenticado, com paginação simples."""
    return crud.get_tasks_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)


@router.post("/", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Cria uma nova tarefa vinculada ao usuário autenticado."""
    return crud.create_task(db, task_in, owner_id=current_user.id)


@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Retorna uma tarefa específica, se pertencer ao usuário autenticado."""
    task = crud.get_task(db, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    return task


@router.patch("/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    task_in: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Atualiza parcialmente uma tarefa (apenas os campos enviados)."""
    task = crud.get_task(db, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    return crud.update_task(db, task, task_in)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Remove uma tarefa do usuário autenticado."""
    task = crud.get_task(db, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    crud.delete_task(db, task)
