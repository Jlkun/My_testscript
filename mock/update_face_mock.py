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

class UpdateFace:
    def __init__(self,**kwargs):
        self._url_scheme = '/UpdateFace'
        self._log = []
        self._return_code='9000'
        self._return_msg= 'success'
        self._taskId= kwargs.get('taskId', '7535f823ba1b44708beef284e1115709')
        self._acceptDate=  kwargs.get('acceptDate', datetime.datetime.now().strftime('%Y%m%d%H%M'))


    def get_url_scheme(self):
        return self._url_scheme

    def mock_response(self, received_url=None, received_request=None):
        logger.info('UpdateFace Mock收到请求')
        response = dict()
        response['resCode'] = self._return_code
        response['resDesc'] = self._return_msg
        response['taskId'] = self._taskId
        response['acceptDate'] = self._acceptDate
        return (response)
