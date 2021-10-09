# -*- coding: utf-8

from common import consts
from common import consts,config_util
from common.string_util import *

config = config_util.getconfig()
class GetPartnerCardList:
    def __init__(self,**kwargs):
        self._user_token = kwargs.get('userToken', '')

    def url(self):
        http_schema = config.get("http_option", "http_schema")
        end_point = config.get("http_option", "wind_router_point")
        return http_schema + '://' + end_point + '/wind/sptcc/1/0/get-partner-card-list'

    def make_payload(self):
        # 组装req_data
        request_body = dict()
        request_body['userToken'] = self._user_token
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