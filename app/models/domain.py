from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pgvector.sqlalchemy import Vector
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    refresh_tokens: Mapped[list[RefreshToken]] = relationship(
        back_populates="user"
    )

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)

    token: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped[User] = relationship(back_populates="refresh_tokens")

class District(Base):
    __tablename__ = "districts"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(120), 
        unique=True, 
        index=True
    )
    state: Mapped[str] = mapped_column(
        String(120),    
        default="Maharashtra", 
        index=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,    
        default=True, 
        nullable=False
    )
    jobs: Mapped[list[JobPosting]] = relationship(
        back_populates="district"
    )
    training_centres: Mapped[list[TrainingCentre]] = relationship(
        back_populates="district"
    )

class Sector(Base):
    __tablename__ = "sectors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(160), 
        unique=True, 
        index=True
    )
    description: Mapped[str | None] = mapped_column(Text())

class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    sector_id: Mapped[int | None] = mapped_column(ForeignKey("sectors.id"), index=True)

class Occupation(Base):
    __tablename__ = "occupations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text())

class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    category: Mapped[str | None] = mapped_column(String(160), index=True)
    description: Mapped[str | None] = mapped_column(Text())
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class Qualification(Base):
    __tablename__ = "qualifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(240), unique=True, index=True)
    nsqf_level: Mapped[int | None] = mapped_column(Integer())
    description: Mapped[str | None] = mapped_column(Text())

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(240), index=True)
    qualification_id: Mapped[int | None] = mapped_column(ForeignKey("qualifications.id"), index=True)
    description: Mapped[str | None] = mapped_column(Text())
    duration_hours: Mapped[int | None] = mapped_column(Integer())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class CourseSkill(Base):
    __tablename__ = "course_skills"
    __table_args__ = (UniqueConstraint("course_id", "skill_id", name="uq_course_skill"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), index=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id", ondelete="CASCADE"), index=True)
    proficiency_level: Mapped[int | None] = mapped_column(Integer())

class TrainingCentre(Base):
    __tablename__ = "training_centres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(240), index=True)
    district_id: Mapped[int] = mapped_column(ForeignKey("districts.id"), index=True)
    centre_type: Mapped[str | None] = mapped_column(String(120))
    total_capacity: Mapped[int | None] = mapped_column(Integer())

    district: Mapped[District] = relationship(back_populates="training_centres")

class JobPosting(Base):
    __tablename__ = "job_postings"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str | None] = mapped_column(String(240), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(240), index=True)
    description: Mapped[str | None] = mapped_column(Text())
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"), index=True)
    occupation_id: Mapped[int | None] = mapped_column(ForeignKey("occupations.id"), index=True)
    sector_id: Mapped[int | None] = mapped_column(ForeignKey("sectors.id"), index=True)
    district_id: Mapped[int | None] = mapped_column(ForeignKey("districts.id"), index=True)
    experience_min_years: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    salary_min: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    salary_max: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)
    source: Mapped[str] = mapped_column(String(120), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    district: Mapped[District | None] = relationship(back_populates="jobs")

class JobSkill(Base):
    __tablename__ = "job_skills"
    __table_args__ = (UniqueConstraint("job_posting_id", "skill_id", name="uq_job_skill"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    job_posting_id: Mapped[int] = mapped_column(ForeignKey("job_postings.id", ondelete="CASCADE"), index=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id", ondelete="CASCADE"), index=True)
    required_proficiency: Mapped[int | None] = mapped_column(Integer())
    extraction_confidence: Mapped[Decimal | None] = mapped_column(Numeric(5, 4))

class EmployerSurvey(Base):
    __tablename__ = "employer_surveys"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"), index=True)
    district_id: Mapped[int | None] = mapped_column(ForeignKey("districts.id"), index=True)
    sector_id: Mapped[int | None] = mapped_column(ForeignKey("sectors.id"), index=True)
    expected_hires_next_12_months: Mapped[int | None] = mapped_column(Integer())
    notes: Mapped[str | None] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class SkillDemandSnapshot(Base):
    __tablename__ = "skill_demand_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), index=True)
    district_id: Mapped[int | None] = mapped_column(ForeignKey("districts.id"), index=True)
    sector_id: Mapped[int | None] = mapped_column(ForeignKey("sectors.id"), index=True)
    period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    demand_count: Mapped[int] = mapped_column(Integer(), default=0)
    demand_score: Mapped[Decimal | None] = mapped_column(Numeric(8, 4))

class SkillSupplySnapshot(Base):
    __tablename__ = "skill_supply_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), index=True)
    district_id: Mapped[int | None] = mapped_column(ForeignKey("districts.id"), index=True)
    period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    supply_count: Mapped[int] = mapped_column(Integer(), default=0)
    supply_score: Mapped[Decimal | None] = mapped_column(Numeric(8, 4))

class SkillGap(Base):
    __tablename__ = "skill_gaps"

    id: Mapped[int] = mapped_column(primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), index=True)
    district_id: Mapped[int | None] = mapped_column(ForeignKey("districts.id"), index=True)
    demand_score: Mapped[Decimal] = mapped_column(Numeric(8, 4))
    supply_score: Mapped[Decimal] = mapped_column(Numeric(8, 4))
    gap_score: Mapped[Decimal] = mapped_column(Numeric(8, 4), index=True)
    priority: Mapped[str] = mapped_column(String(32), index=True)
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    district_id: Mapped[int | None] = mapped_column(ForeignKey("districts.id"), index=True)
    skill_gap_id: Mapped[int | None] = mapped_column(ForeignKey("skill_gaps.id"), index=True)
    recommendation_type: Mapped[str] = mapped_column(String(80), index=True)
    title: Mapped[str] = mapped_column(String(240))
    explanation: Mapped[str] = mapped_column(Text())
    confidence_score: Mapped[Decimal | None] = mapped_column(Numeric(8, 4))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
