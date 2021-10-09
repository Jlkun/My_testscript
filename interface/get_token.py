#! /usr/bin/env python
# encoding=utf-8



import logging
import hashlib
import datetime
from functools import reduce
from common.config_util import getconfig
from common.crypto_util import md5, sign_hmac_sha256
from common.string_util import create_key_value_string
from common.string_util import *
from common.http_utils import HttpUtils

config = getconfig()
logger = logging.getLogger(__name__)


class GetToken:
    def url(self):
        http_schema = config.get("http_option", "http_schema")
        end_point = config.get("http_option", "wind_router_point")
        return http_schema + '://' + end_point + '/wind/sptcc/1/0/get-token'

    def make_payload(self,**kwargs):
        # 组装req_data
        request_body = dict()
        request_body['source'] = 'IOS_SPTCC_01700002'
        request_body['timestamp'] = (datetime.datetime.now()).strftime('%Y%m%d%H%M%S')
        request_body['appUserId'] = kwargs.get('appUserId', None)
        request_body['cardList'] = None
        request_body['appKeyIndex'] = '1'
        request_body['issueFlag'] = '0'

        timestamp = request_body['timestamp']
        app_user_id = request_body['appUserId']
        source = request_body['source']
        card_list = request_body['cardList']
        app_key_index = request_body['appKeyIndex']
        issue_flag = request_body['issueFlag']

        key_source = (timestamp if (timestamp is not None) else '') + (
        app_user_id if (app_user_id is not None) else '') + (source if (source is not None) else '')
        app_key = reduce(lambda x, y: y + x, md5(key_source))
        sign_source = dict()
        if source is not None:
            sign_source['source'] = source
        if timestamp is not None:
            sign_source['timestamp'] = timestamp
        if app_user_id is not None:
            sign_source['appUserId'] = app_user_id
        if card_list is not None:
            sign_source['cardList'] = card_list
        if app_key_index is not None:
            sign_source['appKeyIndex'] = app_key_index
        if issue_flag is not None:
            sign_source['issueFlag'] = issue_flag
        sign_source = create_key_value_string(sign_source)
        sign_source = app_key + '&' + sign_source + '&' + app_key
        sign = kwargs.get('sign', sign_hmac_sha256(sign_source, app_key))
        request_body['sign'] = sign
        return request_body

    def assert_response_data(self, response=None, res_code='0000', res_desc='success'):
        error_count = 0
        error_msg_list = []
        if assert_equal(response.get('resCode', None), res_code) is False:
            error_msg = 'issue-card 应答中的resCode为%s!=%s' % (
                response.get('resCode', None), res_code)
            logger.error(error_msg)
            error_msg_list.append(error_msg)
            error_count += 1
        if assert_equal(response.get('resDesc', None), res_desc) is False:
            error_msg = 'issue-card应答中的resDesc为%s!=%s' % (
                response.get('resDesc', None), res_desc)
            logger.error(error_msg)
            error_msg_list.append(error_msg)
            error_count += 1
        return error_count, error_msg_list

    def execute(self,**kwargs):
        self.error_count = 0
        self.error_msg_list = []
        issue_card_response = HttpUtils.http_post(
            url=self.url(),
            json=self.make_payload(appUserId=kwargs.get('appUserId',None))
        ).json()

        error_count, error_msg_list = self.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True
        # issue_card_response.get('expireTimeStamp', None)
        return issue_card_response.get('token', None)



