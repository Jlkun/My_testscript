# -*- coding: utf-8

from mock.query_card_mock import QueryCard
from common import thread_utils
from common.models_wind import *
from common.string_util import *
from common import consts,config_util,log,exec_remote_server
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from interface.issue_card import WindIssueCard
from interface.get_card_handle_result import GetCardHandleResult
from interface.get_token import GetToken
from common.http_utils import HttpUtils
import unittest
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

        # self.appUserId=random_app_uuid()
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

    def test_TC0055_001(self):
        """
        用例名称:
          查询发卡结果功能正向测试 发卡成功
        """

        get_card_handle_result = GetCardHandleResult(cardNo='3104770002968547777')
        logger.info("发起get_card_handle_result请求")
        issue_card_response=HttpUtils.http_post(
            url=get_card_handle_result.url(),
            json=get_card_handle_result.make_payload()
        ).json()
        error_count, error_msg_list = get_card_handle_result.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True
    def test_TC005_002(self):
        """
              用例名称:
                查询发卡结果功能正向测试 开卡失败
        """

        get_card_handle_result = GetCardHandleResult(cardNo='3104770002853471690', partnerToken='ptoken94385726')
        logger.info("发起issue_card请求")
        issue_card_response = HttpUtils.http_post(
            url=get_card_handle_result.url(),
            json=get_card_handle_result.make_payload()
        ).json()
        error_count, error_msg_list = get_card_handle_result.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True
    def test_TC005_003(self):
        """
        用例名称:
            查询发卡结果功能正向测试 已退卡
        """
        get_card_handle_result = GetCardHandleResult(cardNo='3104770002916537480', partnerToken='ptoken96573842')
        logger.info("发起issue_card请求")
        issue_card_response = HttpUtils.http_post(
            url=get_card_handle_result.url(),
            json=get_card_handle_result.make_payload()
        ).json()
        error_count, error_msg_list = get_card_handle_result.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True

    def test_TC005_004(self):
        """
        用例名称:
          查询发卡结果功能 candy或moka还没有进行结果通知，复旦过来查询状态分别为开卡成功，开卡失败
        """
        mock_thread = thread_utils.MockServerThread(timeount=60000)
        mock_thread.start()
        # get_card_handle_result = GetCardHandleResult(cardNo='', partnerToken='ptoken68732459')#开卡成功

        get_card_handle_result = GetCardHandleResult(cardNo='', partnerToken='ptoken69258473')#开卡成功

        # get_card_handle_result = GetCardHandleResult(cardNo='', partnerToken='ptoken25479683')#开卡失败
        logger.info("发起issue_card请求")
        issue_card_response = HttpUtils.http_post(
            url=get_card_handle_result.url(),
            json=get_card_handle_result.make_payload()
        ).json()
        error_count, error_msg_list = get_card_handle_result.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True

    def test_TC005_005(self):
        """
        用例名称:
           申请开卡测试 userToken为null&''
        """
        get_card_handle_result = GetCardHandleResult(cardNo='3104770002968547777', partnerToken='1111')
        logger.info("发起issue_card请求")
        issue_card_response = HttpUtils.http_post(
            url=get_card_handle_result.url(),
            json=get_card_handle_result.make_payload()
        ).json()
        error_count, error_msg_list = get_card_handle_result.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True
    def test_TC005_006(self):
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
    def test_TC005_007(self):
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


