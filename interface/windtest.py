# -*- coding: utf-8

import json
from common import consts,config_util
from common.config_util import getconfig, getCert
from common.string_util import *
from collections import OrderedDict
from common.crypto_util import sign_rsawithsha256_signature
from common.crypto_util import aes256_gcm_encrypt
from common.crypto_util import aes256_cbc_pkcs7padding_encrypt
import datetime
config = config_util.getconfig()
logger = logging.getLogger(__name__)
config = config_util.getconfig()

class IssueCardFirm:
    def __init__(self,**kwargs):
        self._cardNo = kwargs.get('cardNo', '3104830020100299977')
        self._result = kwargs.get('result', 1)
        self._coBrandCard = kwargs.get('coBrandCard',"0170000506000049")
        self._nonce = kwargs.get('nonce', '20210429160333')
        # self._nonce = kwargs.get('nonce', datetime.datetime.now().strftime('%Y%m%d%H%M'))
        self._keyIndex =kwargs.get('keyIndex','0')

    def url(self):
        return 'http://192.168.110.61:19385/epaytest/fmshnfc/bindcard/issuecardconfirm'

    def make_payload(self):
        # 组装req_data
        request_body = dict()
        request_body['cardNo'] = self._cardNo
        request_body['result'] = self._result
        request_body['coBrandCard'] = self._coBrandCard
        request_body['nonce'] = self._nonce
        request_body['keyIndex'] = self._keyIndex
        request_body['sign'] = self.make_sign()
        return request_body

    def make_sign(self):
        sign_source = OrderedDict()
        sign_source['cardNo'] = self._cardNo
        sign_source['result'] = self._result
        sign_source['coBrandCard'] = self._coBrandCard
        sign_source['cardNo'] = self._cardNo
        sign_source['nonce'] = self._nonce
        sign_source['keyIndex'] = self._keyIndex
        rsa_pri_key_file_name = config.get('keys', 'aliver_1711_fmsh_test_rsa2048pri_key')  #这里是用的合作方私钥签名
        with open(getCert(rsa_pri_key_file_name), "r") as f:
            rsa_pri_key = f.read()
            logger.info(
                ' business-dispcath sign_source:%s' % json.dumps(sign_source).replace('\\', '').replace(' ', ''))
        sign = sign_rsawithsha256_signature(rsa_pri_key,
                                            json.dumps(sign_source).replace('\\', '').replace(' ', '')).upper()
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