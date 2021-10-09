# -*- coding: utf-8

import logging

logger = logging.getLogger(__name__)

class IssueCardConfirm:
    def __init__(self):
        self._url_scheme = '/wind/sptcc/1/0/issue-card'
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
        response['resDesc'] = '0000'
        return (response)
