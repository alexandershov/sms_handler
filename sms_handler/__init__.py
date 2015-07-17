from __future__ import division, print_function

from requests.exceptions import RequestException
import requests

HANDLERS = {}


def null_logger(data, json_resp):
    pass


class Handler(object):
    def send(self, data, logger=null_logger):
        raise NotImplementedError


class HttpHandler(Handler):
    def send(self, data, logger=null_logger):
        """
        :param data: dictionary with GET parameters
        :param logger: callable accepting two dictionary arguments: data and json_resp
        :return: dictionary with response json
        """
        try:
            resp = requests.post(self.base_url, params=self.get_params(data))
            resp.raise_for_status()
        except RequestException as exc:
            json_resp = {'status': 'error', 'message': repr(exc), 'type': 'REQUESTS_ERROR'}
        else:
            json_resp = resp.json()

        logger(data, json_resp)
        if json_resp['status'] == 'error':
            raise GateError(json_resp)

        return json_resp

    def get_params(self, data):
        return data

    @property
    def base_url(self):
        raise NotImplementedError


class GateError(Exception):
    pass


class SmsTrafficHandler(HttpHandler):
    base_url = 'http://smstraffic.ru/super-api/message/'


class SmsCenterHandler(HttpHandler):
    base_url = 'http://smsc.ru/some-api/message/'


def register_handler(name, cls):
    if name in HANDLERS:
        raise ValueError('handler {!r} already exists'.format(name))
    HANDLERS[name] = cls


def unregister_handler(name):
    get_handler(name)  # checking that handler exists
    del HANDLERS[name]


def get_handler(name):
    try:
        make_handler = HANDLERS[name]
    except KeyError:
        raise ValueError('unknown handler: {!r}'.format(name))
    else:
        return make_handler()


register_handler('smstraffic', SmsTrafficHandler)
register_handler('smscenter', SmsCenterHandler)
