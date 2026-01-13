# Data Seeding & Admin Bootstrap

## Product import (Excel)
Files expected in repo root (and copied into container):
- `Wine_list.xlsx`
- `spirits.xlsx`

Commands:
- `python manage.py import_wines --file /app/Wine_list.xlsx`
- `python manage.py import_spirits --file /app/spirits.xlsx`

On Render without shell access:
- Set `RUN_SEED=1` and redeploy.

Notes:
- The import commands use `update_or_create`, so they are safe to re-run.

## Create a superuser (admin)
On Render:
- Set `CREATE_SUPERUSER=1`
- Set `ADMIN_USERNAME`, `ADMIN_PASSWORD` (and optionally `ADMIN_EMAIL`)
- Redeploy

Local (only if your local `DATABASE_URL` points to the same Supabase DB):
- `python manage.py createsuperuser`

## Upload media to Supabase Storage
If using Supabase Storage for media:
- Set `SUPABASE_STORAGE_ENABLED=1` and the required storage env vars
- Set `UPLOAD_MEDIA=1` and redeploy

Manual command:
- `python manage.py upload_media --source /app/media --skip-existing`
