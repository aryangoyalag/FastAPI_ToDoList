from fastapi import APIRouter,Depends,status,HTTPException
import schemas,models,OAuth2,database,hashing
from sqlalchemy.orm import Session,joinedload
from typing import List

router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.post("/create_user")
async def create_user(request: schemas.UserCreate, db: Session = Depends(database.get_db)):
    check_user_by_username = db.query(models.User).filter(models.User.username == request.username).first()
    if check_user_by_username:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"User with username {request.username} already exists.")
    check_user_by_email = db.query(models.User).filter(models.User.email == request.email).first()
    if check_user_by_email:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"User with email {request.email} already exists.")

    new_user = models.User(username=request.username, email=request.email, password=hashing.Hash.bcrypt(request.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {f"{request.username} has been added as a user."}

@router.delete('/delete_user',)
async def delete_user(
    request: schemas.UserCreate,
    db: Session = Depends(database.get_db),
    current_email: str = Depends(OAuth2.get_current_user)
):
    if current_email != request.email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You can only delete your own account.")
    
    # Fetch the user record from the database
    user = db.query(models.User).filter(models.User.username == request.username).first()

    # Check if the user exists and verify the password
    if not user or not hashing.Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong user credentials")
    
    # Delete the user
    db.delete(user)
    db.commit()
    return {"detail": f"User account {request.username} has been deleted."}

# @router.get('/', response_model=List[schemas.ShowUser])
# async def get_all_users_with_tasks(db: Session = Depends(database.get_db)):
#     users = db.query(models.User).options(joinedload(models.User.tasks)).all()
#     return users
