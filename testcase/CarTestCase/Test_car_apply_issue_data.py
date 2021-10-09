# -*- coding: utf-8

from common.models_wind import *
from common import consts,config_util,log,exec_remote_server
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from interface.issue_card import WindIssueCard
from interface.issue_card_verify import WindIssueCardVerify
from interface.get_card_handle_result import GetCardHandleResult
from interface.apply_issue_data import ApplyIssueData
from mock.issue_card_confirm_mock import IssueCardConfirm
from common.thread_utils import MockServerThread, stop_thread
from common.models_wind import *
from common import consts,config_util,log,exec_remote_server
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from interface.get_token import GetToken
from common.string_util import *



from common.http_utils import HttpUtils
import unittest
config = config_util.getconfig()
class TestTC02003001212121(unittest.TestCase):
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


    def test_TC003_00001(self):
        """
        用例名称:
           获取开卡数据接口正向测试
        """
        # 合作方mock
        # IssueCardConfirm()
        # self.mock_thread = MockServerThread(timeount=60000)
        # self.mock_thread.start()
        #开卡请求
        apply_issue_data = ApplyIssueData()
        logger.info("发起issue_card请求")
        issue_card_response=HttpUtils.http_post(
            url=apply_issue_data.url(),
            json=apply_issue_data.make_payload()
        ).json()
        error_count, error_msg_list = apply_issue_data.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True

    def test_TC003_002(self):
        """
        用例名称:
           获取开卡数据接口测试 必传参数为''&null测试，毕传字段缺失
        """
        # 合作方mock
        # IssueCardConfirm()
        # self.mock_thread = MockServerThread(timeount=60000)
        # self.mock_thread.start()
        # 开卡请求
        apply_issue_data = ApplyIssueData(requester='')
        apply_issue_data = ApplyIssueData(requester=None)
        apply_issue_data = ApplyIssueData(pubKey=None)


        apply_issue_data = ApplyIssueData(cardNo="", partnerToken="",coBrandCard="",appCode="",
                                          requester='')

        apply_issue_data = ApplyIssueData(cardNo=self.random_card_num, partnerToken="",
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
    def test_TC003_003(self):
        """
        用例名称:
           获取开卡数据接口测试 公钥地址不匹配
        """
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
    def test_TC003_004(self):
        """
        用例名称:
            获取开卡数据接口测试 coBrandCard 和parnterToken不配对
        """
        IssueCardConfirm()
        self.mock_thread = MockServerThread(timeount=60000)
        self.mock_thread.start()
        # 开卡请求
        apply_issue_data = ApplyIssueData(cardNo=self.random_card_num, partnerToken="newyork001")
        apply_issue_data = ApplyIssueData(cardNo=self.random_card_num, coBrandCard="newyorktype001",partnerToken=self.paetnerToken)
        logger.info("发起issue_card请求")
        issue_card_response = HttpUtils.http_post(
            url=apply_issue_data.url(),
            json=apply_issue_data.make_payload()
        ).json()
        error_count, error_msg_list = apply_issue_data.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True
    def test_TC001_005(self):
        """
        用例名称:
          获取开卡数据接口测试 requester传不存在（或者无效）系统编号
        """
        IssueCardConfirm()
        self.mock_thread = MockServerThread(timeount=60000)
        self.mock_thread.start()
        # 开卡请求
        apply_issue_data = ApplyIssueData(cardNo=self.random_card_num,requester="010010",
                                          partnerToken=self.paetnerToken)
        logger.info("发起issue_card请求")
        issue_card_response = HttpUtils.http_post(
            url=apply_issue_data.url(),
            json=apply_issue_data.make_payload()
        ).json()
        error_count, error_msg_list = apply_issue_data.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True

    def test_TC001_006(self):
        """
        用例名称:
           获取开卡数据接口测试 合作方mock返回失败
        """
        # IssueCardConfirm()
        # self.mock_thread = MockServerThread(timeount=60000)
        # self.mock_thread.start()
        # 开卡请求
        apply_issue_data = ApplyIssueData(cardNo=self.random_card_num,
                                          partnerToken=self.paetnerToken)
        logger.info("发起issue_card请求")
        issue_card_response = HttpUtils.http_post(
            url=apply_issue_data.url(),
            json=apply_issue_data.make_payload()
        ).json()
        error_count, error_msg_list = apply_issue_data.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True

    def test_TC001_007(self):
        """
        用例名称:
           获取开卡数据接口，重新进行获取开卡数据
        """
        apply_issue_data = ApplyIssueData(cardNo="02701459638",
                                          partnerToken="ptoken49765823")
        logger.info("发起issue_card请求")
        issue_card_response = HttpUtils.http_post(
            url=apply_issue_data.url(),
            json=apply_issue_data.make_payload()
        ).json()
        error_count, error_msg_list = apply_issue_data.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True


