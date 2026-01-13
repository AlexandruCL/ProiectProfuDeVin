# Troubleshooting

## Tables exist but data missing
Likely cause: `DATABASE_URL` not set and app is using SQLite inside container.
- Fix: Set Render env var `DATABASE_URL` and redeploy.

## Import didn’t run
- `RUN_SEED` not set to `1|true`.
- Excel not copied into container.

## Superuser not created
- `CREATE_SUPERUSER` not enabled
- Missing `ADMIN_USERNAME` or `ADMIN_PASSWORD`
- Wrong database connection

## Images not loading
### If using Django /media
- Ensure `SERVE_MEDIA=1` (or Render default behavior)

### If using Supabase Storage
- Ensure bucket is public
- Ensure `SUPABASE_STORAGE_ENABLED=1` and required keys are set
- Ensure uploaded object keys match the `ImageField` values stored in DB

Tip:
- Open the image URL in a new tab and check if it’s `/media/...` (served by Django) or `https://<project>.supabase.co/storage/...` (served by Supabase). The failing URL tells you which system is misconfigured.
