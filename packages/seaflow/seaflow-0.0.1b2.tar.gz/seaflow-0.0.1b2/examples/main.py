import json
import os
from celery import Celery

# django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

# app definition
app = Celery('main')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(related_name='actions')

import seaflow
from seaflow.base import Seaflow
from seaflow.consts import StepStates

seaflow.set_celery_app(app)
@Seaflow.action()
def test(self, **params):
    print(json.dumps({'root': self.root.name if self.root else None,
                      'task': self.task.name,
                      'step': self.step.name}))
    if self.step.node.name == 'd1' and self.step.retries < self.step.config.get('max_retries', 0):
        1/0
    return {
        'state': StepStates.SUCCESS,
        'data': {
            'a': [1, 2],
            'o': {'o': 'o'},
            'n': 1,
            's': 's',
            'b': True
        }
    }


