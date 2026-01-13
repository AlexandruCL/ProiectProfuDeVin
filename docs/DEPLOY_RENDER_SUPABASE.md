# Deploy: Render (Docker) + Supabase (Postgres)

## 1) Supabase setup
1. Create a Supabase project.
2. Create / get Postgres connection string.
   - Use the **URI** form: `postgresql://...` and ensure `sslmode=require`.
3. (Optional but recommended) Create a Storage bucket for media, e.g. `media`.

## 2) Render setup
1. Push the repository to GitHub.
2. Render Dashboard → New → Web Service
3. Connect GitHub repo
4. Environment: **Docker**
5. Dockerfile path: `./Dockerfile`

## 3) Render environment variables
Minimum:
- `SECRET_KEY` = strong random secret
- `DEBUG` = `False`
- `DATABASE_URL` = Supabase Postgres connection string

Recommended:
- `ALLOWED_HOSTS` = your Render hostname (e.g. `your-service.onrender.com`)
- `CSRF_TRUSTED_ORIGINS` = `https://your-service.onrender.com`

If you use email:
- `EMAIL_HOST_PASSWORD` = SendGrid API key

Seeding / bootstrap (run once, then disable):
- `RUN_SEED` = `1` (imports wines/spirits from Excel)
- `CREATE_SUPERUSER` = `1` (creates admin from env vars)
- `UPLOAD_MEDIA` = `1` (uploads `/app/media` to Supabase Storage)

See [ENV_VARS.md](ENV_VARS.md) for full reference.

## 4) First deploy sequence (recommended)
1. Set minimum env vars (`SECRET_KEY`, `DEBUG=False`, `DATABASE_URL`).
2. Deploy once. Confirm app boots.
3. Enable one-time toggles:
   - `RUN_SEED=1`
   - `CREATE_SUPERUSER=1` plus `ADMIN_USERNAME` and `ADMIN_PASSWORD`
   - `SUPABASE_STORAGE_ENABLED=1` plus Supabase Storage vars (if using Storage)
   - `UPLOAD_MEDIA=1` (if using Storage)
4. Deploy again. Confirm logs show: import + admin creation + media upload.
5. Turn off one-time toggles (`RUN_SEED=0`, `CREATE_SUPERUSER=0`, `UPLOAD_MEDIA=0`).

## 5) Verifying deploy
- `/admin/` loads
- wine list loads
- product images load
