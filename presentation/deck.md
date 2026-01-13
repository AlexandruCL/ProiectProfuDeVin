# ProiectProfuDeVin — Deployment & Architecture Deck

## Slide 1 — Title
ProiectProfuDeVin
Django e-commerce (wines & spirits)
Deployment on Render + Supabase

## Slide 2 — Problem / Goal
- Deploy Django app reliably
- Use managed Postgres (Supabase)
- Handle static and media assets
- Seed product data automatically

## Slide 3 — High-level Architecture
- Render Web Service (Docker + Gunicorn)
- Supabase Postgres (DATABASE_URL)
- Supabase Storage for images (recommended)

## Slide 4 — Container Startup Flow
- `migrate`
- optional: import wines/spirits (`RUN_SEED`)
- optional: create superuser (`CREATE_SUPERUSER`)
- optional: upload media (`UPLOAD_MEDIA`)
- start Gunicorn

## Slide 5 — Environment Variables
- `DATABASE_URL`, `SECRET_KEY`, `DEBUG=False`
- toggles: `RUN_SEED`, `CREATE_SUPERUSER`, `UPLOAD_MEDIA`
- storage: `SUPABASE_STORAGE_ENABLED`, `SUPABASE_PROJECT_REF`, bucket, S3 keys

## Slide 6 — Data Seeding
- Source: Excel files committed in repo
- Imports are idempotent (`update_or_create`)
- Safe to re-run for updates

## Slide 7 — Media Strategy
Option A: serve `/media` via Django (demo)
Option B: Supabase Storage (recommended)

## Slide 8 — Troubleshooting
- Tables but no data → missing `DATABASE_URL`
- Import skipped → `RUN_SEED` not enabled
- Images broken → storage config / bucket not public / URL mismatch

## Slide 9 — Next Steps
- Lock down secrets
- Add health checks
- Move all media to Supabase Storage
- Add CI/CD checks (lint/tests)
