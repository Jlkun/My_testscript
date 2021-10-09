# -*- coding: utf-8


from common.models_wind import *
from common.string_util import *
from common import consts,config_util,log,exec_remote_server
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from interface.issue_card import WindIssueCard
from interface.notify_card_handle_result import NotifyCardHandleResult
from interface.get_token import GetToken
from common.http_utils import HttpUtils
from interface.issue_card_verify import WindIssueCardVerify
from common.thread_utils import MockServerThread, stop_thread
from common.models_wind import *
from common import consts,config_util,log,exec_remote_server
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from interface.apply_issue_data import ApplyIssueData
from mock.issue_card_confirm_mock import IssueCardConfirm
from common.string_util import *
import unittest
import logging
config = config_util.getconfig()

class TestTC02004001(unittest.TestCase):
    def setUp(self):
        log.setLog()
        # 同步服务器时间
        exec_remote_server.exec_cmd(
            'date -s %s' % (datetime.datetime.now()).strftime('%Y-%m-%d')
        )
        exec_remote_server.exec_cmd(
            'date -s %s' % (datetime.datetime.now()).strftime('%H:%M:%S')
        )
        self.test_finish = False
        self.test_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.error_count = 0
        self.error_msg_list = []
        username = config.get("wind_db", "mariadb_username")
        password = config.get("wind_db", 'mariadb_password')
        host = config.get("wind_db", 'mariadb_host')
        port = config.get("wind_db", 'mariadb_port')
        sid = config.get("wind_db", 'mariadb_dbname')
        wind_connect_string = 'mysql://%s:%s@%s:%s/%s?charset=utf8' % (username, password, host, port, sid)
        wind_engine = create_engine(wind_connect_string, echo="debug")
        self.wind_session = sessionmaker(bind=wind_engine)()
        # self.cardNo='3104770002703491865'#传入之前填入的卡号
        # self.appUserId=random_app_uuid()
        # self.userToken = GetToken().execute()(appUserId=self.appUserId)

        self.appUserId = random_app_uuid()
        self.paetnerToken = paetner_token()
        self.random_card_num = random_card_num()
        self.moka_random_card_num = moka_random_card_num()
        # self.userToken = '1'

        self.userToken = GetToken().execute(appUserId=self.appUserId)
        issue_card = WindIssueCard(userToken=self.userToken)
        logger.info("发起issue_card请求")
        issue_card_response = HttpUtils.http_post(
            url=issue_card.url(),
            json=issue_card.make_payload()
        ).json()

        error_count, error_msg_list = issue_card.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True
        self.req_seq=issue_card_response.get('resData').get('reqSeq')

        issue_card_verify = WindIssueCardVerify(userToken=self.userToken, reqSeq=self.req_seq, partnerToken=self.paetnerToken)
        logger.info("发起issue_card请求")
        issue_card_response = HttpUtils.http_post(
            url=issue_card_verify.url(),
            json=issue_card_verify.make_payload()
        ).json()
        error_count, error_msg_list = issue_card_verify.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True

        IssueCardConfirm()
        self.mock_thread = MockServerThread(timeount=60000)
        self.mock_thread.start()
        # 开卡请求
        apply_issue_data = ApplyIssueData(cardNo=self.random_card_num, partnerToken=self.paetnerToken,
                                          requester='01003')
        logger.info("发起issue_card请求")
        issue_card_response = HttpUtils.http_post(
            url=apply_issue_data.url(),
            json=apply_issue_data.make_payload()
        ).json()
        error_count, error_msg_list = apply_issue_data.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True



    def tearDown(self):
        if self.test_finish:
            logger.info("本次测试error个数为%s" % self.error_count)
            if len(self.error_msg_list) > 0:
                logger.info("本次测试错误信息:")
                for i in self.error_msg_list:
                    logger.error(i)
            self.assertEqual(self.error_count, 0, self.error_msg_list)
        else:
            logger.error("测试中发生异常,测试终止")

    def test_TC004_001(self):
        """
        用例名称:
           通知发卡结果成功
        """
        self.mock_thread = MockServerThread(timeount=60000)
        self.mock_thread.start()
        notify_card_handle_result = NotifyCardHandleResult(cardNo= "31047700"+self.random_card_num)
        # notify_card_handle_result = NotifyCardHandleResult(cardNo="3104770003846913705")
        logger.info("发起issue_card请求")
        notify_card_handle_result_response=HttpUtils.http_post(
            url=notify_card_handle_result.url(),
            json=notify_card_handle_result.make_payload()
        ).json()
        # logger.info("issue_card请求内容:"+notify_card_handle_result_response)
        error_count, error_msg_list = notify_card_handle_result.assert_response_data(notify_card_handle_result_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True

    def test_TC004_002(self):
        """
              用例名称:
                发卡结果通知正向功能测试发卡失败
        """
        # notify_card_handle_result = NotifyCardHandleResult(cardNo= "31047700"+self.random_card_num, result=1)
        notify_card_handle_result = NotifyCardHandleResult(cardNo= "31047700"+self.random_card_num, result=1)
        logger.info("发起issue_card请求")
        notify_card_handle_result_response = HttpUtils.http_post(
            url=notify_card_handle_result.url(),
            json=notify_card_handle_result.make_payload()
        ).json()
        error_count, error_msg_list = notify_card_handle_result.assert_response_data(notify_card_handle_result_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True

    def test_TC004_003(self):
        """
        用例名称:
           发卡结果通知正向功能测试退卡成功
        """
        self.mock_thread = MockServerThread(timeount=60000)
        self.mock_thread.start()
        notify_card_handle_result = NotifyCardHandleResult(cardNo="3104770002146953870",result=2)
        logger.info("发起issue_card请求")
        notify_card_handle_result_response = HttpUtils.http_post(
            url=notify_card_handle_result.url(),
            json=notify_card_handle_result.make_payload()
        ).json()
        error_count, error_msg_list = notify_card_handle_result.assert_response_data(notify_card_handle_result_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True
    def test_TC004_004(self):
        """
        用例名称:
          发卡结果通知传参数为''&null测试，毕传字段缺失
        """
        # self.mock_thread = MockServerThread(timeount=60000)
        # self.mock_thread.start()
        notify_card_handle_result = NotifyCardHandleResult(cardNo="", result=2)
        notify_card_handle_result = NotifyCardHandleResult(cardNo="", result="")

        notify_card_handle_result = NotifyCardHandleResult(cardNo="", result="")
        notify_card_handle_result = NotifyCardHandleResult(cardNo=None, result=None,coBrandCard=None)
        logger.info("发起issue_card请求")
        notify_card_handle_result_response = HttpUtils.http_post(
            url=notify_card_handle_result.url(),
            json=notify_card_handle_result.make_payload()
        ).json()
        error_count, error_msg_list = notify_card_handle_result.assert_response_data(notify_card_handle_result_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True
    def test_TC004_005(self):
        """
        用例名称:
           发卡结果通知coBrandCard无效或者操作结果传3和string类型
        """
        self.mock_thread = MockServerThread(timeount=60000)
        self.mock_thread.start()
        notify_card_handle_result = NotifyCardHandleResult(cardNo="3104770002916537480", result="2")
        # notify_card_handle_result = NotifyCardHandleResult(cardNo="3104770002916537480", result=3)
        logger.info("发起issue_card请求")
        notify_card_handle_result_response = HttpUtils.http_post(
            url=notify_card_handle_result.url(),
            json=notify_card_handle_result.make_payload()
        ).json()
        error_count, error_msg_list = notify_card_handle_result.assert_response_data(notify_card_handle_result_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True
    def test_TC004_006(self):
        """
        用例名称:
           申请开卡测试 coBrandCard为null&''
        """
        issue_card = WindIssueCard(coBrandCard='')
        # issue_card = WindIssueCard(coBrandCard=None)
        logger.info("发起issue_card请求")
        issue_card_response=HttpUtils.http_post(
            url=issue_card.url(),
            json=issue_card.make_payload()
        ).json()
        error_count, error_msg_list = issue_card.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True
    def test_TC004_007(self):
        """
        用例名称:
           申请开卡测试 partnerNo为null&''
        """
        issue_card = WindIssueCard(partnerNo='')
        # issue_card = WindIssueCard(partnerNo=None)
        logger.info("发起issue_card请求")
        issue_card_response=HttpUtils.http_post(
            url=issue_card.url(),
            json=issue_card.make_payload()
        ).json()
        error_count, error_msg_list = issue_card.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True


