import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

app = Celery('application')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'update-popular-tags': {
        'task': 'questions.tasks.update_popular_tags_cache',
        'schedule': crontab(minute=0, hour='*/1'),
    },
    'update-best-members': {
        'task': 'questions.tasks.update_best_members_cache',
        'schedule': crontab(minute=0, hour='*/1'),
    },
}