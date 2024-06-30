from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    email: str
    password: str

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    task_title: str

    class Config:
        orm_mode = True

class Task(TaskBase):
    username: str

    class Config:
        orm_mode = True

class ShowUser(UserBase):
    tasks: List[TaskBase] = []

    class Config:
        orm_mode = True

class ShowTask(BaseModel):
    task_title: str

    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
