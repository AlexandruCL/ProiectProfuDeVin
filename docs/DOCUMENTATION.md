# ProiectProfuDeVin — Full Documentation

## 1) Overview
This repository contains a Django web application (Django 5.x) for listing and purchasing wines and spirits.

Key features seen in codebase:
- Product catalog: wines and spirits
- Shopping cart and orders
- Authentication (Django auth + django-allauth)
- Admin dashboard
- Data seeding from Excel files

## 2) Repo layout (high level)
- `my_project/` — Django project root (contains `manage.py` and apps)
  - `my_project/` — Django settings/urls/wsgi
  - `my_app/` — main Django app (models/views/templates/management commands)
  - `static/` — static assets
  - `templates/` — HTML templates
  - `media/` — media files (images used by products)
- `Dockerfile` — container build for Render
- `entrypoint.sh` — startup script: migrate + optional seed + optional superuser + optional media upload
- `Wine_list.xlsx`, `spirits.xlsx` — Excel sources for seeding products

## 3) Runtime architecture
### 3.1 Services
- Web: Render “Web Service” running Docker container with Gunicorn
- Database: Supabase Postgres (configured via `DATABASE_URL`)
- Media storage (recommended): Supabase Storage via S3-compatible endpoint

### 3.2 Request flow
- Browser → Render URL → Gunicorn → Django
- Static: served by WhiteNoise from `/staticfiles` collected at build time
- Media:
  - Option 1: served by Django via `/media/` (only for small/demo setups)
  - Option 2 (recommended): served directly from Supabase Storage public URLs

## 4) Configuration (settings)
### 4.1 Database
- If `DATABASE_URL` is set: Django uses Supabase Postgres.
- If `DATABASE_URL` is missing: Django falls back to SQLite (`db.sqlite3`).

### 4.2 Static files
- Collected during Docker build using `python manage.py collectstatic --noinput`.
- Served by WhiteNoise.

### 4.3 Media
- `MEDIA_ROOT` is `/app/media` inside container.
- If Supabase Storage is enabled, default storage is switched to Supabase.

See [ENV_VARS.md](ENV_VARS.md) and [MEDIA_STORAGE.md](MEDIA_STORAGE.md).

## 5) Deployment on Render + Supabase
Follow [DEPLOY_RENDER_SUPABASE.md](DEPLOY_RENDER_SUPABASE.md).

## 6) Data seeding & admin user
Follow [DATA_SEEDING.md](DATA_SEEDING.md).

## 7) Operations
Follow [OPERATIONS.md](OPERATIONS.md) and [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
