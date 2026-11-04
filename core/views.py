import logging

import redis
from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET

logger = logging.getLogger(__name__)


@require_GET
def health(request):
    database_status = "ok"
    redis_status = "ok"

    try:
        connection.ensure_connection()
    except Exception:
        logger.exception("Database health check failed")
        database_status = "error"

    redis_client = None
    try:
        redis_client = redis.Redis.from_url(settings.REDIS_URL)
        redis_client.ping()
    except Exception:
        logger.exception("Redis health check failed")
        redis_status = "error"
    finally:
        if redis_client is not None:
            try:
                redis_client.close()
            except Exception:
                logger.exception("Redis client cleanup failed")
                redis_status = "error"

    status_code = (
        200 if database_status == "ok" and redis_status == "ok" else 503
    )
    return JsonResponse(
        {
            "status": "ok" if status_code == 200 else "error",
            "database": database_status,
            "redis": redis_status,
        },
        status=status_code,
    )
