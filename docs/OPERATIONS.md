# Operations (Day 2)

## Logs
- Use Render logs to confirm `migrate`, `RUN_SEED`, `CREATE_SUPERUSER`, and `UPLOAD_MEDIA` steps.

## Deploy safety
- Prefer idempotent startup: migrations are safe; imports use `update_or_create`.
- Turn off one-time toggles after successful run.

## Database migrations
- Migrations run automatically on every boot via `entrypoint.sh`.

## Backups
- Use Supabase backup tooling and exports for Postgres.

## Common maintenance actions
- Add new admin: set `CREATE_SUPERUSER=1` + admin vars, redeploy, then disable.
- Re-run import: set `RUN_SEED=1`, redeploy.
- Upload new images: run upload and ensure DB image paths match.
