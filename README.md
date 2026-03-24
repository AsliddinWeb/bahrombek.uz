# bahrombek.uz

Shaxsiy ilmiy portfolio sayti — FastAPI + Vue 3.

## Tez ishga tushirish

### 1. Backend `.env` sozlash

```bash
cp backend/.env.example backend/.env
# .env faylini tahrirlang
```

### 2. Local ishlab chiqish

**Backend:**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# http://localhost:8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
# http://localhost:5173
```

### 3. Docker bilan ishga tushirish

```bash
# Frontend build
docker compose --profile build run --rm frontend

# Barcha servislarni ishga tushirish
docker compose up -d
```

### 4. SSL sertifikat (Let's Encrypt)

```bash
docker compose --profile ssl run --rm certbot certonly \
  --webroot -w /var/www/certbot \
  -d bahrombek.uz -d www.bahrombek.uz \
  --email your@email.com --agree-tos --no-eff-email
```

Keyin `nginx.conf` da HTTPS blokni ochib, nginx restart qiling.

## Tuzilma

```
backend/
  app/
    main.py        — FastAPI app, CORS, static files
    models.py      — SQLAlchemy modellari
    schemas.py     — Pydantic schemalar
    config.py      — .env sozlamalar
    database.py    — DB engine + session
    routers/
      auth.py      — POST /auth/login → JWT
      publications.py — CRUD + PDF upload + RSS
      profile.py   — Profil + avatar + rezyume
      deps.py      — JWT middleware

frontend/src/
  pages/
    HomePage.vue        — Hero + qiziqishlar + so'nggi maqolalar
    PublicationsPage.vue — Qidiruv + filter + pagination
    AboutPage.vue        — Bio + timeline + mukofotlar
    admin/
      AdminLogin.vue    — JWT login
      AdminLayout.vue   — Sidebar layout
      AdminDashboard.vue — Statistika
      AdminArticles.vue  — CRUD + PDF yuklash
      AdminProfile.vue   — Profil tahrirlash
      AdminSettings.vue  — Sayt sarlavhasi/SEO
  components/
    AppHeader.vue        — Nav + til almashtirish + dark mode
    AppFooter.vue        — Ijtimoiy havolalar
    PublicationCard.vue  — Karta + citation (APA/BibTeX) + abstract toggle
  stores/
    auth.ts    — Pinia: JWT token
    profile.ts — Pinia: profil cache
  i18n/
    uz.json / en.json / ru.json
```

## Admin kirish

- URL: `/admin/login`
- Login/parol: `.env` da `ADMIN_USERNAME` / `ADMIN_PASSWORD`

## API endpointlar

| Method | URL | Tavsif |
|--------|-----|--------|
| POST | `/auth/login` | JWT olish |
| GET | `/publications` | Filtrlash, qidiruv, pagination |
| GET | `/publications/{id}/pdf` | PDF yuklab olish |
| GET | `/publications/rss.xml` | RSS feed |
| GET | `/profile` | Ommaviy profil |
| GET | `/profile/resume` | Rezyume PDF |
| POST | `/admin/publications` | Yangi maqola (JWT) |
| PUT | `/admin/publications/{id}` | Tahrirlash (JWT) |
| DELETE | `/admin/publications/{id}` | O'chirish (JWT) |
| POST | `/admin/publications/{id}/pdf` | PDF yuklash (JWT) |
| PUT | `/admin/profile` | Profil yangilash (JWT) |
| POST | `/admin/profile/avatar` | Rasm yuklash (JWT) |
| POST | `/admin/profile/resume` | Rezyume yuklash (JWT) |
