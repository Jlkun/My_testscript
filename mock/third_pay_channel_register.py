#! /usr/bin/env python
# encoding=utf-8
# Author: shuyiqing
# Date: 2017/8/22
import urllib
import logging
from urllib import parse
from common.string_util import assert_equal
from common.crypto_util import md5 as md5_calculate
# from common.consts import SptcReturnCode, MD5_KEY

logger = logging.getLogger(__name__)

set_response = {}
class ThirdPayChannelRegister:
    def __init__(self):
        self._url_scheme = '/handapp_app/ThirdPartyChannelRegister'
        self._log = []


    def set_response(self, phone, return_code='',
                     return_msg=''):
        set_response_info = dict()
        set_response_info['return_code'] = return_code
        set_response_info['return_msg'] = return_msg
        set_response[phone] = set_response_info

    def get_log(self):
        return self._log

    def get_url_scheme(self):
        return self._url_scheme

    # def verify_md5(self, received_url):
    #     parsed_url = urllib.parse.parse_qs(
    #         (parse.urlparse(url=received_url, scheme='http', allow_fragments=True).query))
    #     create_flag = parsed_url['createFlag'][0] if 'createFlag' in parsed_url else None
    #     phone = parsed_url['phone'][0] if 'phone' in parsed_url else None
    #     channel = parsed_url['channel'][0] if 'channel' in parsed_url else None
    #     type = parsed_url['type'][0] if 'type' in parsed_url else None
    #     code = parsed_url['code'][0] if 'code' in parsed_url else None
    #     md5 = parsed_url['md5'][0] if 'md5' in parsed_url else None
    #     sign_source = ''
    #     if create_flag:
    #         sign_source = sign_source + 'createFlag=' + create_flag + '&'
    #     if phone:
    #         sign_source = sign_source + 'phone=' + phone + '&'
    #     if channel:
    #         sign_source = sign_source + 'channel=' + channel + '&'
    #     if type:
    #         sign_source = sign_source + 'type=' + type + '&'
    #     if code:
    #         sign_source = sign_source + 'code=' + code + '&'
    #     sign_source = sign_source + 'key=' + MD5_KEY
    #     if assert_equal(md5, md5_calculate(sign_source)) is False:
    #         return False
    #     else:
    #         return True

    def mock_response(self, received_url=None, received_request=None):

        logger.error('获取phone失败')
        response = dict()
        response['return_code'] = ''
        response['return_msg'] =''

        return response
