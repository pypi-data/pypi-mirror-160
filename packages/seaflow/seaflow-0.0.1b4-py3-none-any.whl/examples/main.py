import os
import sys

import django

sys.path.append('/Users/chenjian/repos/github.com/seaflow')
from celery import Celery

# django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

# celery app definition
app = Celery()
app.config_from_object('django.conf:settings', namespace='CELERY')

import seaflow
seaflow.set_celery_app(app)

app.autodiscover_tasks(packages=['examples'], related_name='actions', force=True)
