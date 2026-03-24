import os
import math
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
import aiofiles

from app.database import get_db
from app.models import Publication, PublicationType
from app.schemas import (
    PublicationCreate, PublicationUpdate, PublicationOut, PublicationListOut
)
from app.config import settings
from app.routers.deps import require_admin

router = APIRouter(tags=["publications"])


def pub_url(pub: Publication) -> str | None:
    if pub.pdf_path:
        return f"/publications/{pub.id}/pdf"
    return None


# ── Public ────────────────────────────────────────────────────────────────────

@router.get("/publications", response_model=PublicationListOut)
async def list_publications(
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=100),
    year: int | None = None,
    pub_type: PublicationType | None = None,
    language: str | None = None,
    search: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    q = select(Publication).where(Publication.is_published == True)

    if year:
        q = q.where(Publication.year == year)
    if pub_type:
        q = q.where(Publication.pub_type == pub_type)
    if language:
        q = q.where(Publication.language == language)
    if search:
        like = f"%{search}%"
        q = q.where(
            or_(
                Publication.title_uz.ilike(like),
                Publication.title_en.ilike(like),
                Publication.keywords.ilike(like),
                Publication.authors.ilike(like),
            )
        )

    total_q = select(func.count()).select_from(q.subquery())
    total = (await db.execute(total_q)).scalar_one()

    q = q.order_by(Publication.year.desc(), Publication.id.desc())
    q = q.offset((page - 1) * limit).limit(limit)
    items = (await db.execute(q)).scalars().all()

    return PublicationListOut(
        items=items,
        total=total,
        page=page,
        limit=limit,
        pages=math.ceil(total / limit) if total else 1,
    )


@router.get("/publications/{pub_id}", response_model=PublicationOut)
async def get_publication(pub_id: int, db: AsyncSession = Depends(get_db)):
    pub = await db.get(Publication, pub_id)
    if not pub or not pub.is_published:
        raise HTTPException(404, "Maqola topilmadi")
    return pub


@router.post("/publications/{pub_id}/view", status_code=204)
async def increment_view(pub_id: int, db: AsyncSession = Depends(get_db)):
    """Frontend detail sahifaga kirganда chaqiriladi — faqat shunda counter oshadi."""
    pub = await db.get(Publication, pub_id)
    if pub and pub.is_published:
        pub.views += 1
        await db.commit()


@router.get("/publications/{pub_id}/pdf")
async def get_pdf(pub_id: int, db: AsyncSession = Depends(get_db)):
    pub = await db.get(Publication, pub_id)
    if not pub or not pub.pdf_path:
        raise HTTPException(404, "PDF topilmadi")
    path = Path(settings.upload_dir) / pub.pdf_path
    if not path.exists():
        raise HTTPException(404, "Fayl topilmadi")
    return FileResponse(str(path), media_type="application/pdf")


@router.get("/publications/{pub_id}/certificate")
async def get_certificate(pub_id: int, db: AsyncSession = Depends(get_db)):
    pub = await db.get(Publication, pub_id)
    if not pub or not pub.certificate_path:
        raise HTTPException(404, "Sertifikat topilmadi")
    path = Path(settings.upload_dir) / pub.certificate_path
    if not path.exists():
        raise HTTPException(404, "Fayl topilmadi")
    return FileResponse(str(path), media_type="application/pdf", filename=f"certificate_{pub_id}.pdf")


# ── Admin ─────────────────────────────────────────────────────────────────────

@router.get("/admin/publications", response_model=PublicationListOut, dependencies=[Depends(require_admin)])
async def admin_list(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    total = (await db.execute(select(func.count(Publication.id)))).scalar_one()
    q = (
        select(Publication)
        .order_by(Publication.year.desc(), Publication.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )
    items = (await db.execute(q)).scalars().all()
    return PublicationListOut(
        items=items, total=total, page=page, limit=limit,
        pages=math.ceil(total / limit) if total else 1,
    )


@router.post("/admin/publications", response_model=PublicationOut, dependencies=[Depends(require_admin)])
async def create_pub(body: PublicationCreate, db: AsyncSession = Depends(get_db)):
    pub = Publication(**body.model_dump())
    db.add(pub)
    await db.commit()
    await db.refresh(pub)
    return pub


@router.put("/admin/publications/{pub_id}", response_model=PublicationOut, dependencies=[Depends(require_admin)])
async def update_pub(pub_id: int, body: PublicationUpdate, db: AsyncSession = Depends(get_db)):
    pub = await db.get(Publication, pub_id)
    if not pub:
        raise HTTPException(404, "Maqola topilmadi")
    for k, v in body.model_dump().items():
        setattr(pub, k, v)
    await db.commit()
    await db.refresh(pub)
    return pub


@router.delete("/admin/publications/{pub_id}", dependencies=[Depends(require_admin)])
async def delete_pub(pub_id: int, db: AsyncSession = Depends(get_db)):
    pub = await db.get(Publication, pub_id)
    if not pub:
        raise HTTPException(404, "Maqola topilmadi")
    if pub.pdf_path:
        try:
            (Path(settings.upload_dir) / pub.pdf_path).unlink(missing_ok=True)
        except Exception:
            pass
    await db.delete(pub)
    await db.commit()
    return {"ok": True}


@router.post("/admin/publications/{pub_id}/pdf", dependencies=[Depends(require_admin)])
async def upload_pdf(pub_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    pub = await db.get(Publication, pub_id)
    if not pub:
        raise HTTPException(404, "Maqola topilmadi")

    max_bytes = settings.max_pdf_size_mb * 1024 * 1024
    content = await file.read()
    if len(content) > max_bytes:
        raise HTTPException(413, f"PDF hajmi {settings.max_pdf_size_mb}MB dan oshmasligi kerak")

    upload_dir = Path(settings.upload_dir) / "publications"
    upload_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{pub_id}.pdf"
    path = upload_dir / filename

    async with aiofiles.open(str(path), "wb") as f:
        await f.write(content)

    pub.pdf_path = f"publications/{filename}"
    await db.commit()
    return {"pdf_path": pub.pdf_path, "pdf_url": f"/publications/{pub_id}/pdf"}


@router.post("/admin/publications/{pub_id}/certificate", dependencies=[Depends(require_admin)])
async def upload_certificate(pub_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    pub = await db.get(Publication, pub_id)
    if not pub:
        raise HTTPException(404, "Maqola topilmadi")

    max_bytes = settings.max_pdf_size_mb * 1024 * 1024
    content = await file.read()
    if len(content) > max_bytes:
        raise HTTPException(413, f"Fayl hajmi {settings.max_pdf_size_mb}MB dan oshmasligi kerak")

    upload_dir = Path(settings.upload_dir) / "publications"
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename or "cert.pdf").suffix or ".pdf"
    filename = f"{pub_id}_cert{ext}"
    path = upload_dir / filename

    async with aiofiles.open(str(path), "wb") as f:
        await f.write(content)

    pub.certificate_path = f"publications/{filename}"
    await db.commit()
    return {"certificate_path": pub.certificate_path, "certificate_url": f"/publications/{pub_id}/certificate"}


# ── RSS ───────────────────────────────────────────────────────────────────────

@router.get("/publications/rss.xml")
async def rss_feed(db: AsyncSession = Depends(get_db)):
    from feedgen.feed import FeedGenerator
    from io import BytesIO

    q = (
        select(Publication)
        .where(Publication.is_published == True)
        .order_by(Publication.created_at.desc())
        .limit(20)
    )
    pubs = (await db.execute(q)).scalars().all()

    fg = FeedGenerator()
    fg.id("https://bahrombek.uz/publications")
    fg.title("Bahrombek — Publikatsiyalar")
    fg.link(href="https://bahrombek.uz/publications", rel="alternate")
    fg.description("Oxirgi ilmiy maqolalar")

    for pub in pubs:
        fe = fg.add_entry()
        fe.id(f"https://bahrombek.uz/publications?id={pub.id}")
        fe.title(pub.title_en or pub.title_uz)
        fe.description(pub.abstract_en or pub.abstract_uz or "")
        if pub.created_at:
            from datetime import timezone
            fe.published(pub.created_at.replace(tzinfo=timezone.utc))

    rss = fg.rss_str(pretty=True)
    return StreamingResponse(BytesIO(rss), media_type="application/rss+xml")
