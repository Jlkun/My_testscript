# -*- coding: utf-8 -*- 
# ! /usr/bin/env python
# encoding=utf-8
# Author: shuyiqing
# Date: 2020/9/8
import json
import random
import datetime
import logging
from collections import OrderedDict
from common import consts
from common.config_util import getconfig, getCert
from common.config_util import getconfig, getCert
from common.crypto_util import sign_rsawithsha256_signature
from common import string_util

from common import crypto_util
from binascii import b2a_hex, a2b_hex,a2b_base64
import base64
import time
config = getconfig()
logger = logging.getLogger(__name__)

class CyBusinessDispatch:
    def __init__(self, **kwargs):
        self._bn= kwargs.get('bn', "05000050888010010007")
        self._signType = kwargs.get('signType',  "SHA256WithRSA")  #bn
        self._item_num = kwargs.get('itemNum', 1)#
        self._timestamp = kwargs.get('timestamp', str(round(time.time() * 1000)))
        self._keyIndex = kwargs.get('keyIndex', "0")
        #reqData----------------------
        self._phoneNo= kwargs.get('phoneNo',"17691169704") #用户登录手机号
        self._productCode= kwargs.get('productCode',"SPA-V-R-2C-2021-08-DOOOLY") #线上抵用券
        self._cardNo= kwargs.get('cardNo',"") #交通卡卡号
        self._amount= kwargs.get('amount',1000) #金额
        self._orderNo = kwargs.get('orderNo', string_util.order_no())
        self._expireTime= kwargs.get('expireTime',"20210812") #金额

    def url(self):
        http_schema = config.get("http_option", "http_schema")
        end_point = config.get("http_option", "spa_roma_end_point")
        # return http_schema + '://' + end_point + '/spa/roma/changyoyo/2/0/business-dispatch'
        return http_schema + '://' + "192.168.110.68:9032" + '/spa/roma/douli/3/0/business-dispatch'


    def make_sign(self):
        sign_source = OrderedDict()
        sign_source['partnerNo'] = self._partner_no
        sign_source['cardNo'] = self._cardNo
        sign_source['coBrandCard'] = self._cobrand_card
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
        request_body['orderNo'] = self._order_no
        request_body['appId'] = self._app_id
        request_body['itemCode'] = self._item_code
        request_body['itemNum'] = self._item_num
        request_body['phone'] = self._phone
        request_body['timestamp'] = self._timestamp
        request_body['account'] = self._account
        request_body['accountType'] = self._account_type
        request_body['price'] = self._price
        request_body['sign'] = self._sign
        print('-----------------')
        print(request_body)
        print('-----------------')
        return request_body

    def parse_response_parameter(self, response):
        spa_accept_seq = response.get('spaAcceptSeq', None)
        accept_time = response.get('acceptTime', None)
        return spa_accept_seq, accept_time

    def assert_response_data(self, response=None, res_code=consts.TypicalResCode.SUCCESS, res_desc='success'):
        error_count = 0
        error_msg_list = []
        if assert_equal(response.get('retCode', None), res_code) is False:
            error_msg = 'business-dispatch应答中的retCode为%s!=%s' % (
                response.get('retCode', None), res_code)
            logger.error(error_msg)
            error_msg_list.append(error_msg)
            error_count += 1
        if assert_equal(response.get('retMsg', None), res_desc) is False:
            error_msg = 'business-dispatch应答中的retMsg为%s!=%s' % (
                response.get('retMsg', None), res_desc)
            logger.error(error_msg)
            error_msg_list.append(error_msg)
            error_count += 1
        return error_count, error_msg_list