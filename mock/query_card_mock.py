# -*- coding: utf-8
from common import consts
import datetime
import logging
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

class QueryCard:
    def __init__(self,**kwargs):
        self._url_scheme = '/query-card'
        self._log = []
        self._return_code='9000'
        self._return_msg= 'sucess'
        self._fpanMainStatus = kwargs.get('fpanMainStatus', 1)
        self._fpanStatus= kwargs.get('fpanStatus', 3)


    def get_url_scheme(self):
        return self._url_scheme

    def mock_response(self, received_url=None, received_request=None):
        logger.info('query-card Mock收到请求')
        response = dict()
        response['result'] = self._return_code
        response['message'] = self._return_msg
        response['fpanMainStatus'] = self._fpanMainStatus
        response['fpanStatus'] = self._fpanStatus
        return (response)
