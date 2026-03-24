from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import aiofiles

from app.database import get_db
from app.models import Profile, Education, Experience, Award
from app.schemas import ProfileOut, ProfileUpdate
from app.config import settings
from app.routers.deps import require_admin

router = APIRouter(tags=["profile"])


def _profile_query():
    return select(Profile).options(
        selectinload(Profile.educations),
        selectinload(Profile.experiences),
        selectinload(Profile.awards),
    ).limit(1)


async def get_or_create_profile(db: AsyncSession) -> Profile:
    result = await db.execute(_profile_query())
    profile = result.scalar_one_or_none()
    if not profile:
        profile = Profile()
        db.add(profile)
        await db.commit()
        # Re-query with selectinload after creation
        result = await db.execute(_profile_query())
        profile = result.scalar_one()
    return profile


@router.get("/profile", response_model=ProfileOut)
async def get_profile(db: AsyncSession = Depends(get_db)):
    return await get_or_create_profile(db)


@router.get("/profile/resume")
async def get_resume(db: AsyncSession = Depends(get_db)):
    profile = await get_or_create_profile(db)
    if not profile.resume_pdf_path:
        raise HTTPException(404, "Rezyume topilmadi")
    path = Path(settings.upload_dir) / profile.resume_pdf_path
    if not path.exists():
        raise HTTPException(404, "Fayl topilmadi")
    return FileResponse(str(path), media_type="application/pdf", filename="resume.pdf")


@router.put("/admin/profile", response_model=ProfileOut, dependencies=[Depends(require_admin)])
async def update_profile(body: ProfileUpdate, db: AsyncSession = Depends(get_db)):
    profile = await get_or_create_profile(db)

    # Update scalar fields
    scalar_fields = [
        "full_name_uz", "full_name_en", "full_name_ru",
        "bio_uz", "bio_en", "bio_ru",
        "email", "phone", "linkedin", "github", "google_scholar", "orcid",
        "position_uz", "position_en", "position_ru",
        "institution_uz", "institution_en", "institution_ru",
        "research_interests", "site_title", "site_description",
    ]
    for field in scalar_fields:
        val = getattr(body, field, None)
        if val is not None:
            setattr(profile, field, val)

    # Replace nested collections
    if body.educations is not None:
        for edu in list(profile.educations):
            await db.delete(edu)
        for item in body.educations:
            db.add(Education(profile_id=profile.id, **item.model_dump()))

    if body.experiences is not None:
        for exp in list(profile.experiences):
            await db.delete(exp)
        for item in body.experiences:
            db.add(Experience(profile_id=profile.id, **item.model_dump()))

    if body.awards is not None:
        for aw in list(profile.awards):
            await db.delete(aw)
        for item in body.awards:
            db.add(Award(profile_id=profile.id, **item.model_dump()))

    await db.commit()
    result = await db.execute(_profile_query())
    return result.scalar_one()


@router.post("/admin/profile/avatar", dependencies=[Depends(require_admin)])
async def upload_avatar(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    profile = await get_or_create_profile(db)
    content = await file.read()
    ext = Path(file.filename or "avatar.jpg").suffix or ".jpg"

    upload_dir = Path(settings.upload_dir) / "profile"
    upload_dir.mkdir(parents=True, exist_ok=True)
    path = upload_dir / f"avatar{ext}"

    async with aiofiles.open(str(path), "wb") as f:
        await f.write(content)

    profile.avatar_url = f"/uploads/profile/avatar{ext}"
    await db.commit()
    return {"avatar_url": profile.avatar_url}


@router.post("/admin/profile/resume", dependencies=[Depends(require_admin)])
async def upload_resume(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    profile = await get_or_create_profile(db)
    content = await file.read()

    upload_dir = Path(settings.upload_dir) / "profile"
    upload_dir.mkdir(parents=True, exist_ok=True)
    path = upload_dir / "resume.pdf"

    async with aiofiles.open(str(path), "wb") as f:
        await f.write(content)

    profile.resume_pdf_path = "profile/resume.pdf"
    await db.commit()
    return {"resume_url": "/profile/resume"}
