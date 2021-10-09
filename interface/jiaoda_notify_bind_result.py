# -*- coding: utf-8

from common import consts
from common import consts,config_util
from common.string_util import *
import json
import datetime
from common import consts,config_util
from common.config_util import getconfig, getCert
from common.string_util import *
from collections import OrderedDict
from common.crypto_util import sign_rsawithsha256_signature



config = config_util.getconfig()
class JiaoDaNotifyBindResult:
    def __init__(self,**kwargs):
        self._partner_no = kwargs.get('partnerNo', consts.PARTNERNO)
        self._cardNo = kwargs.get('cardNo', '3104770034387610705')
        self._type = kwargs.get('type', 1)
        self._resetFlag = kwargs.get('resetFlag', 1)
        self._nonce = kwargs.get('nonce', (datetime.datetime.now()).strftime('%Y%m%d%H%M%S'))
        self._keyIndex = kwargs.get('keyIndex', '0')

    def url(self):
        http_schema = config.get("http_option", "http_schema")
        end_point = config.get("http_option", "wind_biz_point")
        # return http_schema + '://' + end_point + '/wind/sptcc/1/0/notify-bind-result'
        return "http://192.168.110.68:9039/wind/sptcc/1/1/notify-bind-result"

    def make_payload(self):
        # 组装req_data
        request_body = dict()
        request_body['partnerNo'] = self._partner_no
        request_body['cardNo'] = self._cardNo
        request_body['type'] = self._type
        request_body['resetFlag'] = self._resetFlag
        request_body['nonce'] = self._nonce
        request_body['keyIndex'] = self._keyIndex
        request_body['sign'] = self.make_sign()
        return request_body

    def make_sign(self):
        request_body = OrderedDict()
        request_body['partnerNo'] = self._partner_no
        request_body['cardNo'] = self._cardNo
        request_body['type'] = self._type
        request_body['resetFlag'] = self._resetFlag
        request_body['nonce'] = self._nonce
        request_body['keyIndex'] = self._keyIndex
        rsa_pri_key_file_name = config.get('keys', 'aliver_1711_fmsh_test_rsa2048pri_key')  # 这里是用的合作方私钥签名
        with open(getCert(rsa_pri_key_file_name), "r") as f:
            rsa_pri_key = f.read()
            logger.info(
                ' business-dispcath sign_source:%s' % json.dumps(request_body).replace('\\', '').replace(' ', ''))
        sign = sign_rsawithsha256_signature(rsa_pri_key,
                                            json.dumps(request_body).replace('\\', '').replace(' ', '')).upper()
        return sign

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