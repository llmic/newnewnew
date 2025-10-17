from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# 用户相关模型
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

# 文件相关模型
class FileBase(BaseModel):
    filename: str
    file_size: int

class FileCreate(FileBase):
    file_path: str

class File(FileBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True

# 令牌模型
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None