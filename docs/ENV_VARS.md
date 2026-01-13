# Environment Variables Reference

## Core Django
- `SECRET_KEY` (required in production)
- `DEBUG` (`False` on Render)
- `ALLOWED_HOSTS` (comma-separated)
- `CSRF_TRUSTED_ORIGINS` (comma-separated, include `https://...`)

## Database
- `DATABASE_URL` (Supabase Postgres)

## Email (optional)
- `EMAIL_HOST_PASSWORD` (SendGrid API key)

## Seeding / bootstrap toggles
- `RUN_SEED` = `1|true` to import wines/spirits from Excel on startup
- `CREATE_SUPERUSER` = `1|true` to create admin user on startup
- `UPLOAD_MEDIA` = `1|true` to upload `/app/media` to storage on startup

## Admin user (used when CREATE_SUPERUSER is enabled)
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- `ADMIN_EMAIL` (optional)

## Supabase Storage (media)
Enable:
- `SUPABASE_STORAGE_ENABLED` = `1|true`

Required:
- `SUPABASE_PROJECT_REF` (the `xxxxx` from `https://xxxxx.supabase.co`)
- `SUPABASE_STORAGE_BUCKET` (e.g. `media`)
- `SUPABASE_S3_ACCESS_KEY_ID`
- `SUPABASE_S3_SECRET_ACCESS_KEY`

Optional:
- `SUPABASE_S3_REGION` (defaults to `us-east-1`)

## Media serving fallback
- `SERVE_MEDIA` (default: true on Render). If `0`, Django will not serve `/media/`.
