import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import schemas
import crud
from database import get_db
from auth import get_current_active_user
from pathlib import Path

router = APIRouter(
    prefix="/files",
    tags=["files"]
)

# 确保上传目录存在
UPLOAD_DIRECTORY = "uploads"
Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

@router.post("/upload", response_model=schemas.File)
async def upload_file(
    file: UploadFile = File(...),
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 保存文件
    file_path = f"{UPLOAD_DIRECTORY}/{current_user.id}_{file.filename}"
    file_size = 0
    
    with open(file_path, "wb") as buffer:
        while contents := await file.read(1024 * 1024):  # 1MB chunks
            buffer.write(contents)
            file_size += len(contents)
    
    # 创建文件记录
    file_schema = schemas.FileCreate(
        filename=file.filename,
        file_path=file_path,
        file_size=file_size
    )
    
    return crud.create_file(db=db, file=file_schema, user_id=current_user.id)

@router.get("/", response_model=list[schemas.File])
def read_files(
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    files = crud.get_files(db, user_id=current_user.id, skip=skip, limit=limit)
    return files

@router.get("/{file_id}/download")
def download_file(
    file_id: int,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    file = crud.get_file(db, file_id=file_id, user_id=current_user.id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    if not os.path.exists(file.file_path):
        raise HTTPException(status_code=404, detail="File not found on server")
    
    return FileResponse(
        path=file.file_path,
        filename=file.filename,
        media_type='application/octet-stream'
    )

@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(
    file_id: int,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    file = crud.get_file(db, file_id=file_id, user_id=current_user.id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # 删除文件
    if os.path.exists(file.file_path):
        os.remove(file.file_path)
    
    # 删除数据库记录
    if not crud.delete_file(db, file_id=file_id, user_id=current_user.id):
        raise HTTPException(status_code=500, detail="Failed to delete file")
    
    return None