# Media Storage on Render

## Why images break on Render
Render instances have an ephemeral filesystem. Anything written to disk at runtime (uploads) is not guaranteed to persist across restarts.

## Option A: Serve repo-bundled media via Django (simple)
If all images are shipped in the repo and you do not allow user uploads, you can serve `/media/` via Django.
- Works for demo/small apps
- Not recommended for scale

Control:
- `SERVE_MEDIA=1` to serve `/media/`

## Option B (recommended): Supabase Storage
Store images in Supabase Storage (public bucket) and let `ImageField.url` resolve to Supabase URLs.

Pros:
- Persistent
- Fast delivery (served directly)
- Works across restarts

Required env vars: see [ENV_VARS.md](ENV_VARS.md)

## Option C: Render Persistent Disk
Attach a persistent disk and mount it to your media folder.
- Good middle ground
- Requires paid feature and mount configuration
