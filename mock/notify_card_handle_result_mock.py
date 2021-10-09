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


class NotifyCardHandleResult:
    def __init__(self,**kwargs):
        self._url_scheme = '/notify_card_handle_result'
        self._log = []
        self._return_code='0000'
        self._return_msg= 'success'


    def get_url_scheme(self):
        return self._url_scheme

    def mock_response(self, received_url=None, received_request=None):
        logger.info('NotifyCardHandleResult Mock收到请求')
        response = dict()
        resData = dict()
        response['resCode'] = self._return_code
        response['resDesc'] = self._return_msg

        return response
