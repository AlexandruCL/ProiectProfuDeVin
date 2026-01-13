#!/usr/bin/env sh
set -e

# Run migrations (requires DATABASE_URL to be set in Render)
python manage.py migrate --noinput

# Optional one-shot-ish seed (idempotent update_or_create)
if [ "${RUN_SEED}" = "1" ] || [ "${RUN_SEED}" = "true" ] || [ "${RUN_SEED}" = "TRUE" ]; then
	echo "RUN_SEED enabled: importing wines + spirits from Excel"
	python manage.py import_wines --file /app/Wine_list.xlsx
	python manage.py import_spirits --file /app/spirits.xlsx
fi

# Start Gunicorn
exec gunicorn my_project.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${WEB_CONCURRENCY:-2}
