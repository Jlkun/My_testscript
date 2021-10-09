#! /usr/bin/env python
# encoding=utf-8
# Author: shuyiqing
# Date: 2017/8/22
import urllib
import logging
from urllib import parse

from common.crypto_util import md5 as md5_calculate


logger = logging.getLogger(__name__)

set_response = {}
class VerificationCodeRequest:
    def __init__(self):
        self._url_scheme = '/handapp_app/VerificationCodeRequest'
        self._log = []


    def set_response(self, phone, return_code='',
                     return_msg='', **kwargs):
        set_response_info = dict()
        set_response_info['return_code'] = return_code
        set_response_info['return_msg'] = return_msg
        data = dict()
        data['code'] = kwargs.get('code', 123)
        set_response_info['data'] = data
        set_response[phone] = set_response_info

    def get_log(self):
        return self._log

    def get_url_scheme(self):
        return self._url_scheme



    def mock_response(self, received_url=None, received_request=None):
        logger.info('VerificationCodeRequest Mock收到请求')

        response = dict()
        response['return_code'] =''
        response['return_msg'] = ''


        return response
