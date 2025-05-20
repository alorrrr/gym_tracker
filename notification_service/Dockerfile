FROM python:3.11.6-slim AS builder

WORKDIR /usr/src/app/

ENV PYTHONUNBUFFERED = 1

ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --upgrade pip

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["sh", "-c", "python manage.py migrate --noinput && python -m gunicorn --bind 0.0.0.0:8000 --workers 3 notification_service.wsgi:application"]