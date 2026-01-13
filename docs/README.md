# ProiectProfuDeVin Documentation

This folder contains project documentation intended to be exportable to PDF and usable as a deployment/operations runbook.

## Contents
- [DOCUMENTATION.md](DOCUMENTATION.md) — Complete documentation (single file)
- [DEPLOY_RENDER_SUPABASE.md](DEPLOY_RENDER_SUPABASE.md) — Step-by-step deployment on Render + Supabase
- [ENV_VARS.md](ENV_VARS.md) — Environment variables reference
- [DATA_SEEDING.md](DATA_SEEDING.md) — Importing wines/spirits and uploading media
- [MEDIA_STORAGE.md](MEDIA_STORAGE.md) — Media serving options (Render disk vs Supabase Storage)
- [OPERATIONS.md](OPERATIONS.md) — Day-2 ops: migrations, redeploys, backups, troubleshooting
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Common issues and fixes

## Export to PDF
Pick one:

### Option A: VS Code (easy)
- Install extension “Markdown PDF”
- Open [DOCUMENTATION.md](DOCUMENTATION.md)
- Run “Markdown PDF: Export (pdf)”

### Option B: Pandoc
- Install `pandoc`
- Run from repo root:
  - `pandoc docs/DOCUMENTATION.md -o docs/ProiectProfuDeVin_Documentation.pdf`

## Presentation
See [presentation/README.md](../presentation/README.md) for the deck outline and how to generate a `.pptx` that can be imported into Canva.
