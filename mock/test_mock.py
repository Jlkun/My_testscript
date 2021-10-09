# #! /usr/bin/env python
# # encoding=utf-8
# # Author: shuyiqing
# # Date: 2017/8/22
import re
import logging
from mock.issue_card_confirm_mock import IssueCardConfirm
from mock.third_pay_channel_register import ThirdPayChannelRegister
from mock.verification_code_request import VerificationCodeRequest
from mock.notify_card_handle_result_mock import NotifyCardHandleResult
from mock.update_face_mock import UpdateFace
from mock.query_card_mock import QueryCard
from mock.base_http_mock import BaseHttpMock
from common import config_util
import json
config = config_util.getconfig()
logger = logging.getLogger(__name__)
#
#
# class TestMock(BaseHttpMock):
#
#     # def set_content_type(self, received_url):
#     #     if (re.match(IssueCardConfirm().get_url_scheme(), received_url)) or (
#     #             re.match(IssueCardConfirm().get_url_scheme(), received_url)):
#     #         return 'text/html;charset=utf-8'
#     #     else:
#     #         return 'application/json;charset=utf-8'
#
#     def mock_response(self, received_url=None, received_request=None):
#         response = False
#         if re.match(IssueCardConfirm().get_url_scheme(), received_url):
#             response = IssueCardConfirm().mock_response(received_url, received_request)
#             print(json.loads(json.dumps(response)))
#         elif (re.match(NotifyCardHandleResult().get_url_scheme(), received_url)) :
#             response = NotifyCardHandleResult().mock_response(received_url, received_request)
#         elif (re.match(UpdateFace().get_url_scheme(), received_url)):
#             response = UpdateFace().mock_response(received_url, received_request)
#         elif (re.match(QueryCard().get_url_scheme(), received_url)):
#             response = UpdateFace().mock_response(received_url, received_request)
#         else:
#             response = None
#         return response
#
#     def listen_once(self, port=8080, timeout=None):
#         super(TestMock, self).listen_once(port, timeout)
#
#
# if __name__ == '__main__':
#     mock = TestMock()
#     mock.listen_once(timeout=10.0)










#! /usr/bin/env python
# encoding=utf-8
# Author: shuyiqing
# Date: 2017/8/22
import re
import logging
from mock.issue_card_confirm_mock import IssueCardConfirm
from mock.app_status_phone import GetAppUserStatusByPhone
from mock.notify_card_handle_result_mock import NotifyCardHandleResult
from mock.update_face_mock import UpdateFace
from mock.query_card_mock import QueryCard
from mock.base_http_mock import BaseHttpMock
from common import config_util
from common import config_util

config = config_util.getconfig()
logger = logging.getLogger(__name__)


class TestMock(BaseHttpMock):
    def set_content_type(self, received_url):
        if (re.match(ThirdPayChannelRegister().get_url_scheme(), received_url)) or (
                re.match(VerificationCodeRequest().get_url_scheme(), received_url)):
            return 'text/html;charset=utf-8'
        else:
            return 'application/json;charset=utf-8'

    def mock_response(self, received_url=None, received_request=None):
        response = False
        if re.match(IssueCardConfirm().get_url_scheme(), received_url):
            response = IssueCardConfirm().mock_response(received_url, received_request)
        # elif (re.match(GetSptcCardStatus().get_url_scheme1(), received_url)) or (
        # re.match(GetSptcCardStatus().get_url_scheme2(), received_url)):
        #     response = GetSptcCardStatus().mock_response(received_url, received_request)
        # elif re.match(GetAppStatusByPhone().get_url_scheme(), received_url):
        #     response = GetAppStatusByPhone().mock_response(received_url, received_request)
        # # elif re.match(RechargeDee().get_url_scheme(), received_url):
        # #     response = RechargeDee().mock_response(received_url, received_request)
        # elif re.match(RechargeDeeByUuid().get_url_scheme(), received_url):
        #     response = RechargeDeeByUuid().mock_response(received_url, received_request)
        # elif re.match(RechargeQry().get_url_scheme(), received_url):
        #     response = RechargeQry().mock_response(received_url, received_request)
        elif re.match(QueryCard().get_url_scheme(), received_url):
            response = QueryCard().mock_response(received_url, received_request)
        elif re.match(ThirdPayChannelRegister().get_url_scheme(), received_url):
            response = ThirdPayChannelRegister().mock_response(received_url, received_request)
        elif re.match(UpdateFace().get_url_scheme(), received_url):
            response = UpdateFace().mock_response(received_url, received_request)
        elif re.match(NotifyCardHandleResult().get_url_scheme(), received_url):
            response = NotifyCardHandleResult().mock_response(received_url, received_request)
        elif re.match(IssueCardConfirm().get_url_scheme(), received_url):
            response = IssueCardConfirm().mock_response(received_url, received_request)
        elif re.match(GetAppUserStatusByPhone().get_url_scheme(), received_url):
            response = GetAppUserStatusByPhone().mock_response(received_url, received_request)
        else:
            response = None
        return response

    def listen_once(self, port=8080, timeout=None):
        super(TestMock, self).listen_once(port, timeout)


if __name__ == '__main__':
    mock = TestMock()
    mock.listen_once(timeout=10.0)
