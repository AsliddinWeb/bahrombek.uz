from sqlalchemy import (
    Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class PublicationType(str, enum.Enum):
    journal = "journal"
    conference = "conference"
    book = "book"
    patent = "patent"
    thesis = "thesis"


class Publication(Base):
    __tablename__ = "publications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title_uz: Mapped[str] = mapped_column(String(512))
    title_en: Mapped[str] = mapped_column(String(512))
    title_ru: Mapped[str | None] = mapped_column(String(512), nullable=True)
    abstract_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    abstract_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    abstract_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    authors: Mapped[str] = mapped_column(String(512))
    journal: Mapped[str | None] = mapped_column(String(256), nullable=True)
    year: Mapped[int] = mapped_column(Integer)
    volume: Mapped[str | None] = mapped_column(String(256), nullable=True)
    issue: Mapped[str | None] = mapped_column(String(256), nullable=True)
    pages: Mapped[str | None] = mapped_column(String(64), nullable=True)
    doi: Mapped[str | None] = mapped_column(String(256), nullable=True)
    isbn: Mapped[str | None] = mapped_column(String(64), nullable=True)
    url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    pub_type: Mapped[PublicationType] = mapped_column(
        Enum(PublicationType), default=PublicationType.journal
    )
    language: Mapped[str] = mapped_column(String(8), default="en")
    keywords: Mapped[str | None] = mapped_column(String(512), nullable=True)
    content_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    pdf_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    certificate_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    views: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name_uz: Mapped[str] = mapped_column(String(256), default="")
    full_name_en: Mapped[str] = mapped_column(String(256), default="")
    full_name_ru: Mapped[str | None] = mapped_column(String(256), nullable=True)
    bio_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    bio_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    bio_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    email: Mapped[str | None] = mapped_column(String(256), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    linkedin: Mapped[str | None] = mapped_column(String(256), nullable=True)
    github: Mapped[str | None] = mapped_column(String(256), nullable=True)
    google_scholar: Mapped[str | None] = mapped_column(String(256), nullable=True)
    orcid: Mapped[str | None] = mapped_column(String(64), nullable=True)
    resume_pdf_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    position_uz: Mapped[str | None] = mapped_column(String(256), nullable=True)
    position_en: Mapped[str | None] = mapped_column(String(256), nullable=True)
    position_ru: Mapped[str | None] = mapped_column(String(256), nullable=True)
    institution_uz: Mapped[str | None] = mapped_column(String(256), nullable=True)
    institution_en: Mapped[str | None] = mapped_column(String(256), nullable=True)
    institution_ru: Mapped[str | None] = mapped_column(String(256), nullable=True)
    research_interests: Mapped[str | None] = mapped_column(Text, nullable=True)  # comma-separated
    site_title: Mapped[str] = mapped_column(String(256), default="Bahrombek — Ilmiy ishlar")
    site_description: Mapped[str | None] = mapped_column(Text, nullable=True)

    educations: Mapped[list["Education"]] = relationship(
        "Education", back_populates="profile", cascade="all, delete-orphan"
    )
    experiences: Mapped[list["Experience"]] = relationship(
        "Experience", back_populates="profile", cascade="all, delete-orphan"
    )
    awards: Mapped[list["Award"]] = relationship(
        "Award", back_populates="profile", cascade="all, delete-orphan"
    )


class Education(Base):
    __tablename__ = "educations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"))
    degree: Mapped[str] = mapped_column(String(256))
    institution: Mapped[str] = mapped_column(String(256))
    year_start: Mapped[int | None] = mapped_column(Integer, nullable=True)
    year_end: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="educations")


class Experience(Base):
    __tablename__ = "experiences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"))
    position: Mapped[str] = mapped_column(String(256))
    organization: Mapped[str] = mapped_column(String(256))
    year_start: Mapped[int | None] = mapped_column(Integer, nullable=True)
    year_end: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="experiences")


class Award(Base):
    __tablename__ = "awards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"))
    title: Mapped[str] = mapped_column(String(256))
    organization: Mapped[str | None] = mapped_column(String(256), nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="awards")
