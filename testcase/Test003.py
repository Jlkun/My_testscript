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
class TestTC02003001(unittest.TestCase):
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

        self.appUserId = random_app_uuid()
        self.paetnerToken = paetner_token()
        self.random_card_num = random_card_num()
        self.moka_random_card_num = moka_random_card_num()
        self.userToken='1'


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


        # self.userToken='d49ef8ecfd7142b38c26f9833ccc7f8d'
        # self.req_seq = '2103241639141893001'

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


    def test_TC003_001(self):
        """
        用例名称:
           获取开卡数据接口正向测试
        """
        # 合作方mock
        # IssueCardConfirm()
        # self.mock_thread = MockServerThread(timeount=60000)
        # self.mock_thread.start()
        #开卡请求
        apply_issue_data = ApplyIssueData(cardNo=self.moka_random_card_num,partnerToken=self.paetnerToken ,requester='01003')

        #candy第一次打我们接口，candy没收到消息回复，但合作方已经通知数据库状态已经翻了，这时候他再打我们给他返回相同数据，但这时候不通知合作方了  （已测试
        # apply_issue_data = ApplyIssueData(cardNo="3104770003597140638",partnerToken="ptoken45783296" ,requester='01005')
        # 开卡成功之后，卡片已经迁出，candy打我们不传parterntoken进行恢复测试，其他照传  （有问题）
        # apply_issue_data = ApplyIssueData(cardNo="3104770003846913705",partnerToken=None ,requester='01005')
        # apply_issue_data = ApplyIssueData(cardNo="3104770003597140638",partnerToken="ptoken45783296" ,requester='01005')
        #退卡之后 candy再过来获取开卡数据
        # apply_issue_data = ApplyIssueData(cardNo="3104770002853471690",partnerToken="ptoken59723468")
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


