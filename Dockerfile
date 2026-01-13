# syntax=docker/dockerfile:1

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python deps
COPY my_project/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app source
COPY my_project/ /app/

# Copy seed Excel files (committed at repo root)
COPY spirits.xlsx Wine_list.xlsx /app/

# Collect static at build time (uses a safe build-only secret)
ENV DJANGO_SETTINGS_MODULE=my_project.settings \
    DEBUG=False \
    SECRET_KEY=build-time-secret
RUN python manage.py collectstatic --noinput

# Run
EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
