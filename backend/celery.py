import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.prod')

app = Celery('Backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule                      = {
    'update-template-status': {
        'task'      : 'competitions.tasks.update_competitions_status',
        'schedule'  : 5 * 60,
        'args'      : ()
    },
}
app.conf.timezone                           = 'UTC'

