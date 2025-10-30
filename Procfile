web: daphne -b 0.0.0.0 -p $PORT backend.asgi:application
worker: celery -A backend worker -l INFO -E -B --concurrency 2