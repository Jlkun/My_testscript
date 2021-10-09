
# -*- coding: utf-8


from common.models_wind import *
from common.string_util import *
from common import consts,config_util,log,exec_remote_server
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from interface.issue_card import WindIssueCard
from interface.skd_apply_issue_data import Skd_Apply_Issue_Data
from interface.get_token import GetToken
from common.http_utils import HttpUtils
import unittest
from common.thread_utils import MockServerThread, stop_thread
import logging
config = config_util.getconfig()

class TestTC02001001(unittest.TestCase):
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

        self.appUserId=random_app_uuid()
        # self.userToken = GetToken().execute(appUserId=self.appUserId)


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

    def test_TC00sdk_001(self):
        """
        用例名称:

        """

        # self.mock_thread = MockServerThread(timeount=60000)
        # self.mock_thread.start()

        skd_apply_issue_data = Skd_Apply_Issue_Data(cardNo="3104770094479439604",partnerToken=self.appUserId)
        logger.info("发起skd_apply_issue_data请求")
        issue_card_response=HttpUtils.http_post(
            url=skd_apply_issue_data.url(),
            json=skd_apply_issue_data.make_payload()
        ).json()

        error_count, error_msg_list = skd_apply_issue_data.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True
    def test_TC001_002(self):
        """
        用例名称:
           申请开卡测试 token过期
        """
        issue_card = WindIssueCard(userToken=self.userToken)
        logger.info("发起issue_card请求")
        issue_card_response=HttpUtils.http_post(
            url=issue_card.url(),
            json=issue_card.make_payload()
        ).json()
        error_count, error_msg_list = issue_card.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True
    def test_TC001_003(self):
        """
        用例名称:
           申请开卡测试 无效卡类型
        """
        issue_card = WindIssueCard(userToken=self.userToken)
        logger.info("发起issue_card请求")
        issue_card_response=HttpUtils.http_post(
            url=issue_card.url(),
            json=issue_card.make_payload()
        ).json()
        error_count, error_msg_list = issue_card.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True
    def test_TC001_004(self):
        """
        用例名称:
           申请开卡测试 无效合作方
        """
        issue_card = WindIssueCard(userToken=self.userToken)
        logger.info("发起issue_card请求")
        issue_card_response=HttpUtils.http_post(
            url=issue_card.url(),
            json=issue_card.make_payload()
        ).json()
        error_count, error_msg_list = issue_card.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True
    def test_TC001_005(self):
        """
        用例名称:
           申请开卡测试 userToken为null&''
        """
        issue_card = WindIssueCard(userToken='')
        # issue_card = WindIssueCard(userToken=None)
        logger.info("发起issue_card请求")
        issue_card_response=HttpUtils.http_post(
            url=issue_card.url(),
            json=issue_card.make_payload()
        ).json()
        error_count, error_msg_list = issue_card.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True
    def test_TC001_006(self):
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
    def test_TC001_007(self):
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


