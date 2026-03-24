# Server deployment qo'llanmasi

> Ubuntu 22.04 / 24.04 server uchun. Boshqa Linux distributivlarda ham ishlaydi.

---

## 1. Server tayyorlash

```bash
# Tizimni yangilash
sudo apt update && sudo apt upgrade -y

# Kerakli paketlar
sudo apt install -y git curl
```

---

## 2. Docker o'rnatish

```bash
# Docker o'rnatish skripti
curl -fsSL https://get.docker.com | sudo sh

# Joriy foydalanuvchini docker guruhiga qo'shish (sudo ishlatmaslik uchun)
sudo usermod -aG docker $USER

# O'zgarish kuchga kirishi uchun qayta ulanish kerak
# exit qilib, SSH orqali qayta kiring
exit
```

Qayta kirganingizdan so'ng tekshirish:
```bash
docker --version        # Docker version 27.x.x
docker compose version  # Docker Compose version v2.x.x
```

---

## 3. Loyihani clone qilish

```bash
# /var/www papkasiga joylashtirish (yoki o'zingiz istagan joy)
sudo mkdir -p /var/www
sudo chown $USER:$USER /var/www

cd /var/www
git clone https://github.com/YOUR_USERNAME/bahrombek.uz.git
cd bahrombek.uz
```

---

## 4. Environment fayllarini sozlash

### 4.1 Root `.env`

```bash
cp .env.example .env
nano .env
```

```env
APP_PORT=80
APP_PORT_SSL=443

POSTGRES_DB=bahrombek_db
POSTGRES_USER=bahrombek
POSTGRES_PASSWORD=KUCHLI_PAROL_YOZING
```

> **Muhim:** `POSTGRES_PASSWORD` ni o'zgartiring. Hech qachon `dbpassword123` qoldirmang.

### 4.2 Backend `.env`

```bash
cp backend/.env.example backend/.env
nano backend/.env
```

```env
ADMIN_USERNAME=bahrombek
ADMIN_PASSWORD=ADMIN_PAROLINGIZ
JWT_SECRET=UZUN_TASODIFIY_STRING_YOZING

DATABASE_URL=postgresql+asyncpg://bahrombek:KUCHLI_PAROL_YOZING@db/bahrombek_db

UPLOAD_DIR=./uploads
MAX_PDF_SIZE_MB=20
CORS_ORIGINS=https://bahrombek.uz,https://www.bahrombek.uz
```

> `POSTGRES_PASSWORD` root `.env` dagi bilan bir xil bo'lishi kerak!

Tasodifiy JWT_SECRET yaratish:
```bash
openssl rand -hex 32
```

### 4.3 nginx.conf ni domeyn bilan sozlash

```bash
nano nginx.conf
```

`server_name` qatorini o'z domeyningizga o'zgartiring:
```nginx
server_name bahrombek.uz www.bahrombek.uz;
```

---

## 5. Ishga tushirish

```bash
docker compose up -d --build
```

Bir necha daqiqa kutish kerak (birinchi marta image build qiladi).

Tekshirish:
```bash
docker compose ps
```

Barcha containerlar `Up` holatida bo'lishi kerak:
```
NAME                    STATUS
bahrombekuz-db-1        Up (healthy)
bahrombekuz-backend-1   Up
bahrombekuz-frontend-1  Up
bahrombekuz-nginx-1     Up
```

Brauzerda `http://SERVER_IP` yoki `http://bahrombek.uz` ochib tekshiring.

---

## 6. SSL sertifikat (HTTPS)

DNS sozlangan bo'lishi kerak: `bahrombek.uz → server IP`.

### 6.1 Certbot bilan sertifikat olish

```bash
docker compose run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email sizning@email.com \
  --agree-tos \
  --no-eff-email \
  -d bahrombek.uz \
  -d www.bahrombek.uz
```

### 6.2 nginx.conf da HTTPS yoqish

```bash
nano nginx.conf
```

HTTP serverda redirect qo'shing:
```nginx
server {
    listen 80;
    server_name bahrombek.uz www.bahrombek.uz;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}
```

HTTPS server blokini uncomment qiling (faylning pastki qismida):
```nginx
server {
    listen 443 ssl;
    server_name bahrombek.uz www.bahrombek.uz;

    ssl_certificate     /etc/letsencrypt/live/bahrombek.uz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/bahrombek.uz/privkey.pem;

    location /api/ {
        proxy_pass http://backend/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 25M;
    }

    location /uploads/ {
        proxy_pass http://backend/uploads/;
        proxy_set_header Host $host;
    }

    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

nginx ni qayta yuklash:
```bash
docker compose restart nginx
```

### 6.3 Sertifikatni avtomatik yangilash (cron)

```bash
crontab -e
```

Quyidagini qo'shing:
```
0 3 * * * cd /var/www/bahrombek.uz && docker compose run --rm certbot renew --quiet && docker compose restart nginx
```

---

## 7. Yangilanish (update)

GitHub dan yangi o'zgarishlarni serverga olish:

```bash
cd /var/www/bahrombek.uz

# Yangi kodni olish
git pull

# Qayta build qilish va ishga tushirish
docker compose up -d --build
```

> Database o'chmasligi uchun faqat `--build` flag bilan ishlating. `down` yozmang.

---

## 8. Foydali buyruqlar

```bash
# Loglarni ko'rish
docker compose logs -f backend
docker compose logs -f nginx

# Barcha loglar
docker compose logs -f

# Containerlarni to'xtatish (database saqlanadi)
docker compose stop

# Qayta ishga tushirish
docker compose restart

# Faqat backend ni qayta build qilish
docker compose build backend
docker compose up -d backend
```

---

## 9. Backup

Database backup olish:
```bash
docker compose exec db pg_dump -U bahrombek bahrombek_db > backup_$(date +%Y%m%d).sql
```

Backup dan tiklash:
```bash
cat backup_20260101.sql | docker compose exec -T db psql -U bahrombek bahrombek_db
```

Uploads papkasini backup qilish:
```bash
tar -czf uploads_$(date +%Y%m%d).tar.gz backend/uploads/
```

---

## Muammo chiqsa

**Sayt ochilmayapti:**
```bash
docker compose ps          # containerlar ishlaptyaptimi?
docker compose logs nginx  # nginx xatosi bormi?
```

**Backend xatosi:**
```bash
docker compose logs backend
```

**DB ulanmayapti:**
```bash
# backend/.env dagi DATABASE_URL ni tekshiring
# POSTGRES_PASSWORD ikkala .env da bir xilmi?
```
