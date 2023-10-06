import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'new_posts_weekly_sending': {
        'task': 'news.tasks.send_weekly_mail' ,
        'schedule': crontab(),
    },
}

app.autodiscover_tasks()