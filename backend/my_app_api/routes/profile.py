from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, UserProfile
from ..schemas import ProfileResponse, ProfileCreate
from ..auth import get_current_user
from ..utils.file_upload import process_avatar

profile = APIRouter(prefix="/profile", tags=["profile"])

@profile.get("/", response_model=ProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.profile:
        # Создание профиля если не существует
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(current_user)
    
    return current_user.profile

@profile.put("/", response_model=ProfileResponse)
def update_profile(
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.profile:
        profile = UserProfile(user_id=current_user.id, **profile_data.dict())
        db.add(profile)
    else:
        for field, value in profile_data.dict(exclude_unset=True).items():
            setattr(current_user.profile, field, value)
    
    db.commit()
    db.refresh(current_user.profile)
    return current_user.profile