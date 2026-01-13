#!/usr/bin/env sh
set -e

echo "Starting Django container";

# On Render you *must* set DATABASE_URL (otherwise you'll be using SQLite in-container)
if [ -n "${RENDER_EXTERNAL_HOSTNAME}" ] && [ -z "${DATABASE_URL}" ]; then
	echo "ERROR: DATABASE_URL is not set. Configure Supabase connection string in Render env vars.";
	exit 1
fi

# Run migrations (requires DATABASE_URL to be set in Render)
python manage.py migrate --noinput

# Optional one-shot-ish seed (idempotent update_or_create)
if [ "${RUN_SEED}" = "1" ] || [ "${RUN_SEED}" = "true" ] || [ "${RUN_SEED}" = "TRUE" ]; then
	echo "RUN_SEED enabled: importing wines + spirits from Excel"
	if [ ! -f /app/Wine_list.xlsx ]; then
		echo "ERROR: /app/Wine_list.xlsx not found in container";
		exit 1
	fi
	if [ ! -f /app/spirits.xlsx ]; then
		echo "ERROR: /app/spirits.xlsx not found in container";
		exit 1
	fi
	python manage.py import_wines --file /app/Wine_list.xlsx
	python manage.py import_spirits --file /app/spirits.xlsx
	echo "Import completed"
else
	echo "RUN_SEED not enabled; skipping import"
fi

# Optional superuser creation (idempotent)
if [ "${CREATE_SUPERUSER}" = "1" ] || [ "${CREATE_SUPERUSER}" = "true" ] || [ "${CREATE_SUPERUSER}" = "TRUE" ]; then
	echo "CREATE_SUPERUSER enabled: ensuring admin user exists"
	python manage.py ensure_superuser
	echo "Superuser ensured"
else
	echo "CREATE_SUPERUSER not enabled; skipping"
fi

# Start Gunicorn
exec gunicorn my_project.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${WEB_CONCURRENCY:-2}
