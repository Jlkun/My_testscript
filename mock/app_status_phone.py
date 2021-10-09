# -*- coding: utf-8

import logging
from common.models_wind import *
from common.string_util import *
from common import consts,config_util,log,exec_remote_server
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from interface.issue_card import WindIssueCard
from interface.notify_bind_result import NotifyBindResult
from interface.get_token import GetToken
from common.http_utils import HttpUtils
import unittest
import logging
logger = logging.getLogger(__name__)

class GetAppUserStatusByPhone:
    def __init__(self):
        self._url_scheme = '/gas-sptcc-broker/biz/1/0/get-app-user-status-by-phone'
        self._log = []

    def set_response(self, return_code='0000',
                     return_msg='成功', **kwargs):
        set_response_info = dict()
        set_response_info['return_code'] = return_code
        set_response_info['return_msg'] = return_msg
        resData = dict()
        resData['code'] = kwargs.get('userId', )
        resData['coBrandCard'] = kwargs.get('coBrandCard', )
        resData['subCoBrandCard'] = kwargs.get('subCoBrandCard', )
        resData['deKey'] = kwargs.get('deKey', )
        resData['parnterData'] = kwargs.get('parnterData', )
        resData['extraData'] = kwargs.get('extraData', )
        resData['nonce'] = kwargs.get('nonce', )
        resData['keyIndex'] = kwargs.get('keyIndex', )
        resData['sign'] = kwargs.get('sign', )

    def get_url_scheme(self):
        return self._url_scheme

    def mock_response(self, received_url=None, received_request=None):
        logger.info('issue-card Mock收到请求')
        response = dict()
        response['resCode'] = '0000'
        response['resDesc'] = 'success'
        response['appUserID'] =random_app_uuid()
        response['userStatus'] = '00'
        return (response)
