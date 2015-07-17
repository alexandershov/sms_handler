# coding: utf-8

from __future__ import division, print_function

import json

from mock import Mock
import pytest
import responses

from sms_handler import get_handler, SmsTrafficHandler, GateError

DATA = {'login': 'john', 'psw': '123', 'phone': '555 1234'}
OK_JSON = {'status': 'ok', 'phone': '555 1234'}
ERROR_JSON = {'status': 'error', 'phone': '555 1234', 'error_code': 3500,
              'error_msg': u'Невозможно отправить сообщение указанному абоненту'}


@responses.activate
def test_handler():
    logger = send(DATA, OK_JSON)
    logger.assert_called_once_with(DATA, OK_JSON)


@responses.activate
def test_gate_error_response():
    logger = Mock()
    with pytest.raises(GateError):
        send(DATA, ERROR_JSON, logger=logger)
    # checking that errors are logged
    logger.assert_called_once_with(DATA, ERROR_JSON)


@responses.activate
def test_requests_error():
    logger = Mock()
    with pytest.raises(GateError):
        send(DATA, OK_JSON, status=500, logger=logger)
    # checking that errors are logged even in case of RequestException
    # we don't check call args, because RequestException text probably is not the same
    # in different requests versions
    assert logger.call_count == 1


def send(data, resp_json, status=200, logger=None):
    handler = get_handler('smstraffic')
    responses.add(responses.POST, handler.base_url,
                  body=json.dumps(resp_json), status=status)
    if logger is None:
        logger = Mock()
    handler.send(data, logger=logger)
    return logger
