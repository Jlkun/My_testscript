# -*- coding: utf-8

from common import consts
from common import consts,config_util
from common.string_util import *
import datetime
from collections import OrderedDict
from common.crypto_util import sign_rsawithsha256_signature
import datetime

import json
from common import consts,config_util
from common.config_util import getconfig, getCert
from common.string_util import *
from collections import OrderedDict
from common.crypto_util import sign_rsawithsha256_signature
import datetime
config = config_util.getconfig()
class CarNotifyCardHandleResult:
    def __init__(self, **kwargs):
        self._coBrandCard = kwargs.get('coBrandCard', '0170000506000049')
        self._subCoBrandCard = kwargs.get('subCoBrandCard', '0170000506000049')
        self._result = kwargs.get('result', 0)
        self._cardNo = kwargs.get('cardNo', '3104770094479439605')
        self._partnerToken = kwargs.get('partnerToken', '1111')
        self._remark = kwargs.get('remark', '1111')
        self._nonce = kwargs.get ('nonce', datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        self._keyIndex = kwargs.get('keyIndex', '0')

    def make_payload(self):
        # 组装req_data
        request_body = dict()
        request_body['coBrandCard'] = self._coBrandCard
        request_body['subCoBrandCard'] = self._subCoBrandCard
        request_body['result'] = self._result
        request_body['cardNo'] = self._cardNo
        request_body['partnerToken'] = self._partnerToken
        request_body['remark'] = self._remark
        request_body['nonce'] = self._nonce
        request_body['keyIndex'] = self._keyIndex
        request_body['sign'] = self.make_sign()
        print("发送数据")
        print(request_body)
        return request_body

    def make_sign(self):
        sign_source = OrderedDict()
        sign_source['coBrandCard'] = self._coBrandCard
        sign_source['subCoBrandCard'] = self._subCoBrandCard
        sign_source['result'] = self._result
        sign_source['cardNo'] = self._cardNo
        sign_source['partnerToken'] = self._partnerToken
        sign_source['remark'] = self._remark
        sign_source['nonce'] = self._nonce
        sign_source['keyIndex'] = self._keyIndex
        print("代签数据")
        print(sign_source)
        rsa_pri_key_file_name = config.get('keys', 'aliver_1711_fmsh_test_rsa2048pri_key')  # 这里是用的合作方私钥签名
        with open(getCert(rsa_pri_key_file_name), "r") as f:
            rsa_pri_key = f.read()
            logger.info(
                ' business-dispcath sign_source:%s' % json.dumps(sign_source).replace('\\', '').replace(' ', ''))
        sign = sign_rsawithsha256_signature(rsa_pri_key,
                                            json.dumps(sign_source).replace('\\', '').replace(' ', '')).upper()
        return sign

    # def __init__(self,**kwargs):
    #     self._coBrandCard= kwargs.get('coBrandCard', '0170000506000049')
    #     self._subCoBrandCard= kwargs.get('subCoBrandCard', '0170000506000049')
    #     self._result = kwargs.get('result', 0)
    #     self._cardNo = kwargs.get('cardNo', '3104770094479439605')
    #     self._partnerToken = kwargs.get('partnerToken', "1111")
    #     self._remark = kwargs.get('remark', "1111")
    #     self._nonce = kwargs.get('nonce', (datetime.datetime.now()).strftime('%Y%m%d%H%M%S'))
    #     self._keyIndex = kwargs.get('keyIndex', '0')
    #
    # def make_payload(self):
    #     # 组装req_data
    #     request_body = dict()
    #     request_body['coBrandCard'] = self._coBrandCard
    #     request_body['subCoBrandCard'] = self._subCoBrandCard
    #     request_body['result'] = self._result
    #     request_body['cardNo'] = self._cardNo
    #     request_body['partnerToken'] = self._partnerToken
    #     request_body['remark'] = self._remark
    #     request_body['nonce'] = self._nonce
    #     request_body['keyIndex'] = self._keyIndex
    #     request_body['sign'] = self.make_sign()
    #     return request_body
    #
    # def make_sign(self):
    #     sign_source = OrderedDict()
    #     sign_source['coBrandCard'] = self._coBrandCard
    #     sign_source['subCoBrandCard'] = self._subCoBrandCard
    #     sign_source['result'] = self._result
    #     sign_source['cardNo'] = self._cardNo
    #     sign_source['partnerToken'] = self._partnerToken
    #     sign_source['remark'] = self._remark
    #     sign_source['nonce'] = self._nonce
    #     sign_source['keyIndex'] = self._keyIndex
    #     rsa_pri_key_file_name = config.get('keys', 'aliver_1711_fmsh_test_rsa2048pri_key')
    #     with open(getCert(rsa_pri_key_file_name), "r") as f:
    #         rsa_pri_key = f.read()
    #         logger.info(
    #             ' business-dispcath sign_source:%s' % json.dumps(sign_source).replace('\\', '').replace(' ', ''))
    #     sign = sign_rsawithsha256_signature(rsa_pri_key,
    #                                         json.dumps(sign_source).replace('\\', '').replace(' ', '')).upper()
    #     return sign


    def url(self):
        http_schema = config.get("http_option", "http_schema")
        end_point = config.get("http_option", "wind_biz_point")
        # return http_schema + '://' + end_point + '/wind/sptcc/1/0/notify-card-handle-result'
        return 'http://47.103.98.173:8099/fdcard/card/notifyCardHandleResult'

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