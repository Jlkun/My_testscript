# -*- coding: utf-8

from common import consts
from common import consts,config_util
from common.string_util import *
import codecs
import json
import datetime
from common import consts,config_util
from common.config_util import getconfig, getCert
from common.string_util import *
from collections import OrderedDict
from common.crypto_util import sign_rsawithsha256_signature
config = config_util.getconfig()
class Skd_Apply_Issue_Data:
    def __init__(self,**kwargs):
        str='30819F300D06092A864886F70D010101050003818D0030818902818100B410AA991A715B6D64F0FF0329A0F19BDB6341FDF855098CA6A676D388C7A0BA4522C84EFE2565AB14E283FD553C24E43E5F6B28706CCD2ABA44AE52D47CDC249F43B1EAF6C9AFCCD530A332747925A1951B2367C53A53198D18E9805D9F55E0D069CBC2B3D8BD942A89B60B079C3316045EEC1A19A19AFFE2E7F6FA7F9B3DBB0203010001'
        self._pub_key = kwargs.get('pubKey',str)
        self._cardNo = kwargs.get('cardNo', "3104770094479439605")
        self._coBrandCard = kwargs.get('coBrandCard', 'NJSMK.SAIC')
        self._partnerToken = kwargs.get('partnerToken', '1113')
        self._requester = kwargs.get('requester', '10001')
        self._appCode= kwargs.get('appCode', 'sdk_10001')
        self._deviceProvider= kwargs.get('deviceProvider', '03000004')
        self._nonce= kwargs.get('nonce', (datetime.datetime.now()).strftime('%Y%m%d%H%M%S'))
        self._keyIndex= kwargs.get('keyIndex', '0')



    def url(self):
        http_schema = config.get("http_option", "http_schema")
        end_point = config.get("http_option", "wind_biz_point")
        # return http_schema + '://' + end_point + '/wind/sptcc/1/0/apply-issue-data'
        # return "https://192.168.110.68:9039/wind/NJ-KW/1/1/apply-issue-data"
        # return "https://wind.uat.nfcos.cn:8196/wind/NJ-KW/1/1/apply-issue-data"

        # http_schema = config.get("http_option", "http_schema")
        # end_point = "192.168.110.68:9039"

        return http_schema + '://' + end_point + '/wind/NJ-KW/1/1/apply-issue-data'



    def make_sign(self):
        sign_source = OrderedDict()
        sign_source['pubKey'] = self._pub_key
        sign_source['cardNo'] = self._cardNo
        sign_source['coBrandCard'] = self._coBrandCard
        sign_source['partnerToken'] = self._partnerToken
        sign_source['requester'] = self._requester
        sign_source['appCode'] = self._appCode
        sign_source['deviceProvider'] = self._deviceProvider
        sign_source['nonce'] = self._nonce
        sign_source['keyIndex'] = self._keyIndex
        rsa_pri_key_file_name = config.get('keys', 'aliver_1711_fmsh_test_rsa2048pri_key')  # 这里是用的合作方私钥签名
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
        request_body['pubKey'] = self._pub_key
        request_body['cardNo'] = self._cardNo
        request_body['coBrandCard'] = self._coBrandCard
        request_body['partnerToken'] = self._partnerToken
        request_body['requester'] = self._requester
        request_body['deviceProvider'] = self._deviceProvider
        request_body['appCode'] = self._appCode
        request_body['nonce'] = self._nonce
        request_body['keyIndex'] = self._keyIndex
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