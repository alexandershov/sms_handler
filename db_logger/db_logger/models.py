from __future__ import division, print_function

import json

from django.db import models

from sms_handler import get_handler


class LogEntry(models.Model):
    data = models.TextField()
    response = models.TextField()
    d_time = models.DateTimeField(auto_now_add=True)


def db_logger(data, json_resp):
    LogEntry.objects.create(data=json.dumps(data), response=json.dumps(json_resp))


def use_db_logger():
    handler = get_handler('smstraffic')
    handler.send({'user': 'john'}, db_logger)
