# -*- coding: utf-8

import json
from common import consts,config_util
from common.config_util import getconfig, getCert
from common.string_util import *
from collections import OrderedDict
from common.crypto_util import sign_rsawithsha256_signature
import datetime

config = config_util.getconfig()
class WindIssueCardVerify:
    def __init__(self,**kwargs):
        self._partner_no = kwargs.get('partnerNo', consts.PARTNERNO)
        self._cobrand_card = kwargs.get('coBrandCard', consts.COBRANDCARD)
        self._partner_token = kwargs.get('partnerToken', '')
        self._user_token = kwargs.get('userToken', '')
        self._req_seq= kwargs.get('reqSeq', '')
        self._nonce = kwargs.get('nonce',(datetime.datetime.now()).strftime('%Y%m%d%H%M%S'))
        self._key_index = kwargs.get('keyIndex', '0')
    def url(self):
        http_schema = config.get("http_option", "http_schema")
        end_point = config.get("http_option", "wind_router_point")
        return http_schema + '://' + end_point + '/wind/sptcc/1/0/issue-card-verify'

    def make_sign(self):
        sign_source = OrderedDict()
        sign_source['partnerNo'] = self._partner_no
        sign_source['coBrandCard'] = self._cobrand_card
        sign_source['partnerToken'] = self._partner_token
        sign_source['userToken'] = self._user_token
        sign_source['reqSeq'] = self._req_seq
        sign_source['nonce'] = self._nonce
        sign_source['keyIndex'] = self._key_index
        rsa_pri_key_file_name = config.get('keys', 'aliver_1711_fmsh_test_rsa2048pri_key')
        with open(getCert(rsa_pri_key_file_name), "r") as f:
            rsa_pri_key = f.read()
            logger.info(
                ' business-dispcath sign_source:%s' % json.dumps(sign_source).replace('\\', '').replace(' ', ''))
        sign = sign_rsawithsha256_signature(rsa_pri_key,
                                            json.dumps(sign_source).replace('\\', '').replace(' ', '')).upper()
        return sign

    def make_payload(self):
        # 组装req_data
        request_body = dict()
        request_body['partnerNo'] = self._partner_no
        request_body['coBrandCard'] = self._cobrand_card
        request_body['partnerToken'] = self._partner_token
        request_body['userToken'] = self._user_token
        request_body['reqSeq'] = self._req_seq
        request_body['nonce'] = self._nonce
        request_body['keyIndex'] = self._key_index
        request_body['sign'] = self.make_sign()
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