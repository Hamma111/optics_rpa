from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.signals import setup_logging

# setting the Django settings module.
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object(settings, namespace='CELERY')


@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig

    from django.conf import settings

    dictConfig(settings.LOGGING)


# Looks up for task modules in Django applications and loads them
app.autodiscover_tasks()
app.conf.beat_schedule = {}
