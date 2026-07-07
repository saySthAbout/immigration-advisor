from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import UserProfile
from app.db.session import get_db
from app.schemas.profile import ProfileCreateRequest, ProfileResponse

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.post("", response_model=ProfileResponse)
def create_profile(request: ProfileCreateRequest, db: Session = Depends(get_db)) -> UserProfile:
    profile = UserProfile(**request.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile(profile_id: int, db: Session = Depends(get_db)) -> UserProfile:
    profile = db.get(UserProfile, profile_id)
    if profile is None:
        raise HTTPException(404, "프로필을 찾을 수 없습니다.")
    return profile
