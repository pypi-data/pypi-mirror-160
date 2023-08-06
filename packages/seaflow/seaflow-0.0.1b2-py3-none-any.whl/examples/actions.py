import json

from seaflow.consts import StepStates
from seaflow.base import Seaflow

print(1)
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
