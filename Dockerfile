FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements/ requirements/
RUN pip install --no-cache-dir -r requirements/dev.txt \
    && addgroup --system app \
    && adduser --system --ingroup app app

COPY . .
RUN chown -R app:app /app

USER app

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
