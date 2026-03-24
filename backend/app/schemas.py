from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models import PublicationType


# ── Auth ──────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── Publication ───────────────────────────────────────────────────────────────

class PublicationBase(BaseModel):
    title_uz: str
    title_en: str
    title_ru: Optional[str] = None
    abstract_uz: Optional[str] = None
    abstract_en: Optional[str] = None
    abstract_ru: Optional[str] = None
    authors: str
    journal: Optional[str] = None
    year: int
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    doi: Optional[str] = None
    isbn: Optional[str] = None
    url: Optional[str] = None
    pub_type: PublicationType = PublicationType.journal
    language: str = "en"
    keywords: Optional[str] = None
    content_uz: Optional[str] = None
    content_en: Optional[str] = None
    content_ru: Optional[str] = None
    is_published: bool = True


class PublicationCreate(PublicationBase):
    pass


class PublicationUpdate(PublicationBase):
    pass


class PublicationOut(PublicationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pdf_path: Optional[str] = None
    certificate_path: Optional[str] = None
    views: int = 0
    created_at: datetime
    updated_at: datetime

    @property
    def has_pdf(self) -> bool:
        return self.pdf_path is not None


class PublicationListOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[PublicationOut]
    total: int
    page: int
    limit: int
    pages: int


# ── Education / Experience / Award ────────────────────────────────────────────

class EducationBase(BaseModel):
    degree: str
    institution: str
    year_start: Optional[int] = None
    year_end: Optional[int] = None
    description: Optional[str] = None
    order: int = 0


class EducationCreate(EducationBase):
    pass


class EducationOut(EducationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ExperienceBase(BaseModel):
    position: str
    organization: str
    year_start: Optional[int] = None
    year_end: Optional[int] = None
    description: Optional[str] = None
    order: int = 0


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceOut(ExperienceBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class AwardBase(BaseModel):
    title: str
    organization: Optional[str] = None
    year: Optional[int] = None
    description: Optional[str] = None
    order: int = 0


class AwardCreate(AwardBase):
    pass


class AwardOut(AwardBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ── Profile ───────────────────────────────────────────────────────────────────

class ProfileBase(BaseModel):
    full_name_uz: str = ""
    full_name_en: str = ""
    full_name_ru: Optional[str] = None
    bio_uz: Optional[str] = None
    bio_en: Optional[str] = None
    bio_ru: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    google_scholar: Optional[str] = None
    orcid: Optional[str] = None
    position_uz: Optional[str] = None
    position_en: Optional[str] = None
    position_ru: Optional[str] = None
    institution_uz: Optional[str] = None
    institution_en: Optional[str] = None
    institution_ru: Optional[str] = None
    research_interests: Optional[str] = None
    site_title: str = "Bahrombek — Ilmiy ishlar"
    site_description: Optional[str] = None


class ProfileUpdate(ProfileBase):
    educations: Optional[list[EducationCreate]] = None
    experiences: Optional[list[ExperienceCreate]] = None
    awards: Optional[list[AwardCreate]] = None


class ProfileOut(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    avatar_url: Optional[str] = None
    resume_pdf_path: Optional[str] = None
    educations: list[EducationOut] = []
    experiences: list[ExperienceOut] = []
    awards: list[AwardOut] = []
