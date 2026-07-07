"""SQLAlchemy ORM 모델.

PRD 3.1(온보딩 및 유저 프로필 입력 대시보드)의 정량 데이터 입력 폼과 3.3의
체크리스트 진행률을 저장한다. 로그인/인증은 아직 PRD에 명시되어 있지 않아
UserProfile은 별도 회원가입 없이 프로필 레코드 자체로 존재한다.
"""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    age: Mapped[int] = mapped_column(Integer)
    education_level: Mapped[str] = mapped_column(String(50))  # High School/Bachelor's/Master's/Doctorate
    years_of_experience: Mapped[float] = mapped_column(Float)
    language_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    origin_continent: Mapped[str] = mapped_column(String(50))
    desired_country: Mapped[str | None] = mapped_column(String(3), nullable=True)  # ISO3, 선택 입력
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    checklist_items: Mapped[list["ChecklistItem"]] = relationship(back_populates="user_profile")


class ChecklistItem(Base):
    """PRD 3.3 기능 7 - 이민 준비 체크리스트 진행률 저장."""

    __tablename__ = "checklist_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_profile_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"))
    task_description: Mapped[str] = mapped_column(String(500))
    is_completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_profile: Mapped["UserProfile"] = relationship(back_populates="checklist_items")
