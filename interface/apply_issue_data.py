# -*- coding: utf-8

from common import consts
from common import consts,config_util
from common.string_util import *
import codecs

config = config_util.getconfig()
class ApplyIssueData:
    def __init__(self,**kwargs):
        str='30819F300D06092A864886F70D010101050003818D0030818902818100B410AA991A715B6D64F0FF0329A0F19BDB6341FDF855098CA6A676D388C7A0BA4522C84EFE2565AB14E283FD553C24E43E5F6B28706CCD2ABA44AE52D47CDC249F43B1EAF6C9AFCCD530A332747925A1951B2367C53A53198D18E9805D9F55E0D069CBC2B3D8BD942A89B60B079C3316045EEC1A19A19AFFE2E7F6FA7F9B3DBB0203010001'
        self._pub_key = kwargs.get('pubKey',str)
        # self._card_no = kwargs.get('cardNo', random_card_num())
        self._card_no = kwargs.get('cardNo', "94479439605")
        # self._cobrand_card = kwargs.get('coBrandCard', consts.COBRANDCARD)
        self._cobrand_card = kwargs.get('coBrandCard', "0170000506000049")
        self._requester = kwargs.get('requester', "0170000506000049")
        self._parnter_token = kwargs.get('partnerToken', '1111')
        self._requester = kwargs.get('requester', '01003')#再测一个moka的 不需要补位 01005
        self._app_code= kwargs.get('appCode', '111')

    #RSA公钥，大写HexString

    def url(self):
        http_schema = config.get("http_option", "http_schema")
        end_point = "192.168.110.68:9039"
        # return http_schema + '://' + end_point + '/wind/NJ-KW/1/1/apply-issue-data'
        return http_schema + '://' + end_point + '/wind/sptcc/1/0/apply-issue-data'

    def make_payload(self):
        # 组装req_data
        request_body = dict()
        request_body['pubKey'] = self._pub_key
        request_body['cardNo'] = self._card_no
        request_body['coBrandCard'] = self._cobrand_card
        request_body['partnerToken'] = self._parnter_token
        request_body['requester'] = self._requester
        request_body['appCode'] = self._app_code
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