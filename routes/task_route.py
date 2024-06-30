from fastapi import APIRouter,Depends,status,HTTPException
import schemas,models,OAuth2,database
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix='/task',
    tags=['Tasks']
)


@router.post('/')
async def create_task(Task_Title:str, db: Session = Depends(database.get_db),
    current_email: str = Depends(OAuth2.get_current_user)):
    check_task = db.query(models.Task).filter(models.Task.task_title == Task_Title).first()
    if check_task:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Task with title '{Task_Title}' already exists. Choose another title.")
    user = db.query(models.User).filter(models.User.email==current_email).first()
    new_task = models.Task(task_title=Task_Title, username=user.username)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return f"Task '{Task_Title}' added successfully by {user.username}."

@router.post('/delete')
async def delete_task(Task_Title : str,db: Session = Depends(database.get_db),
    current_email: str = Depends(OAuth2.get_current_user)):
    user = db.query(models.User).filter(models.User.email==current_email).first()
    check_task = db.query(models.Task).filter(models.Task.task_title == Task_Title,models.Task.username == user.username)
    if not check_task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Task with title '{Task_Title}' created by User '{user.username} exists.")
    
    check_task.delete(synchronize_session=False)
    db.commit()
    return f"Task with title '{Task_Title}' by User '{user.username}' has been deleted."

@router.get('/', response_model=List[schemas.ShowTask])
async def get_tasks(db: Session = Depends(database.get_db), current_email: str = Depends(OAuth2.get_current_user)):
    
    user = db.query(models.User).filter(models.User.email == current_email).first()
    if not user.username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Username '{user.username}' not found.")
    tasks = db.query(models.Task).join(models.User).filter(models.User.username == user.username).all()
    return [{"task_title": task.task_title} for task in tasks]
