# -*- coding: utf-8

import json
from common import consts,config_util
from common.config_util import getconfig, getCert
from common.string_util import *
from collections import OrderedDict
from common.crypto_util import sign_rsawithsha256_signature
import datetime

config = config_util.getconfig()
class ChangeUserCardSubType:
    def __init__(self,**kwargs):
        self._nonce = kwargs.get('nonce', (datetime.datetime.now()).strftime('%Y%m%d%H%M%S'))
        self._key_index = kwargs.get('keyIndex', '0')
        self._partnerNo = kwargs.get('partnerNo', consts.PARTNERNO)
        self._card_No = kwargs.get('cardNo', "")
        self._coBrandCard = kwargs.get('coBrandCard', "fudan001")
        self._subCoBrandCard = kwargs.get('subCoBrandCard', "fudan001")
        self._newSubCoBrandCard = kwargs.get('newSubCoBrandCard', "fudan002")
        # self._cardHandleCode = kwargs.get('cardHandleCode', "fudan001")


    def url(self):
        http_schema = config.get("http_option", "http_schema")
        end_point = config.get("http_option", "wind_biz_point")
        return http_schema + '://' + end_point + '/wind/sptcc/1/0/change-user-card-sub-type'

    def make_sign(self):
        sign_source = OrderedDict()
        sign_source['nonce'] = self._nonce
        sign_source['keyIndex'] = self._key_index
        sign_source['partnerNo'] = self._partnerNo
        sign_source['cardNo'] = self._card_No
        sign_source['coBrandCard'] = self._coBrandCard
        sign_source['subCoBrandCard'] = self._subCoBrandCard
        sign_source['newSubCoBrandCard'] = self._newSubCoBrandCard
        rsa_pri_key_file_name = config.get('keys', 'aliver_1711_fmsh_test_rsa2048pri_key')
        with open(getCert(rsa_pri_key_file_name), "r") as f:
            rsa_pri_key = f.read()
            logger.info(
                ' business-dispcath sign_source:%s' % json.dumps(sign_source).replace('\\', '').replace(' ', ''))
        sign = sign_rsawithsha256_signature(rsa_pri_key,
                                            json.dumps(sign_source).replace('\\', '').replace(' ', '')).upper()
        return sign

    def make_payload(self):
        # ??????req_data
        request_body = dict()

        request_body['nonce'] = self._nonce
        request_body['keyIndex'] = self._key_index
        request_body['sign'] = self.make_sign()
        request_body['partnerNo'] = self._partnerNo
        request_body['cardNo'] = self._card_No
        request_body['coBrandCard'] = self._coBrandCard
        request_body['subCoBrandCard'] = self._subCoBrandCard
        request_body['newSubCoBrandCard'] = self._newSubCoBrandCard


        return request_body

    def assert_response_data(self, response=None, res_code='0000', res_desc='success'):
        error_count = 0
        error_msg_list = []
        if assert_equal(response.get('resCode', None), res_code) is False:
            error_msg = 'issue-card ????????????resCode???%s!=%s' % (
                response.get('resCode', None), res_code)
            logger.error(error_msg)
            error_msg_list.append(error_msg)
            error_count += 1
        if assert_equal(response.get('resDesc', None), res_desc) is False:
            error_msg = 'issue-card????????????resDesc???%s!=%s' % (
                response.get('resDesc', None), res_desc)
            logger.error(error_msg)
            error_msg_list.append(error_msg)
            error_count += 1
        return error_count, error_msg_list