# -*- coding: utf-8


import json as js
import requests
import logging
from common import consts
logger = logging.getLogger(__name__)


class HttpUtils:
    @staticmethod
    def http_post(url, data=None, json=None, **kwargs):
        logging.info('>>> Request Method: POST')
        logger.info('>>> Request Url: \r\n %s' % url)
        if json:
            logger.info('>>> Request Payload: \r\n %s' % js.dumps(json, indent=2, ensure_ascii=False))
        elif data:
            logger.info('>>> Request Payload: \r\n %s' % data)
        else:
            logger.info('>>> Request Payload: \r\n None')
        if kwargs.get('headers'):
            logger.info('>>> Request headers: \r\n %s' % kwargs.get('headers'))

        response = requests.post(url, data=data, json=json, **kwargs)
        logging.info('<<< Status Code: %s' % response.status_code)
        if response.status_code != consts.HttpStatusCode.NO_ERROR:
            logger.error('Http Status Code Not Retrun 200!')
        try:
            logging.info(
                '<<< Response content: \r\n %s' % js.dumps(js.loads(response.text), indent=2, ensure_ascii=False))
        except ValueError:
            logging.info('<<< Response content: \r\n %s' % response.text.encode('utf-8'))
        return response