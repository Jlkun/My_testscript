# -*- coding: utf-8


from common.models_wind import *
from common import consts,config_util,log,exec_remote_server
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from interface.issue_card import WindIssueCard
from interface.issue_card_verify import WindIssueCardVerify
from common.string_util import *
from interface.get_token import GetToken

from common.http_utils import HttpUtils
import unittest
config = config_util.getconfig()
class TestTC02002001(unittest.TestCase):
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
        self.userToken = GetToken().execute(appUserId=self.appUserId)
        #
        # issue_card = WindIssueCard(userToken=self.userToken)
        # logger.info("发起issue_card请求")
        # issue_card_response = HttpUtils.http_post(
        #     url=issue_card.url(),
        #     json=issue_card.make_payload()
        # ).json()
        # # logger.info("issue_card请求内容:" + issue_card_response)
        # error_count, error_msg_list = issue_card.assert_response_data(issue_card_response)
        # self.error_count = self.error_count + error_count
        # self.error_msg_list.extend(error_msg_list)
        # self.test_finish = True
        # self.req_seq=issue_card_response.get('resData').get('reqSeq')

        # self.userToken='d49ef8ecfd7142b38c26f9833ccc7f8d'
        self.req_seq='2103241639141893001'



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


    def test_TC002_001(self):
        """
        用例名称:
           开卡参数校验正向测试
        """
        issue_card_verify = WindIssueCardVerify(userToken=self.userToken,reqSeq=self.req_seq,partnerToken='555')
        logger.info("发起issue_card请求")
        issue_card_response=HttpUtils.http_post(
            url=issue_card_verify.url(),
            json=issue_card_verify.make_payload()
        ).json()
        error_count, error_msg_list = issue_card_verify.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True

    def test_TC002_002(self):
        """
        用例名称:
          开卡参数校验 token过期,必传参数为''&null测试，毕传字段缺失
        """
        issue_card_verify = WindIssueCardVerify(userToken=None, reqSeq=self.req_seq, partnerToken='333')
        issue_card_verify = WindIssueCardVerify(userToken="", reqSeq=self.req_seq, partnerToken='333')
        issue_card_verify = WindIssueCardVerify(userToken=self.userToken, reqSeq="", partnerToken='333')
        issue_card_verify = WindIssueCardVerify(userToken=self.userToken, reqSeq=None, partnerToken='333')
        issue_card_verify = WindIssueCardVerify(userToken=self.userToken, reqSeq=self.req_seq, partnerToken='222',nonce='',partnerNo="")
        issue_card_verify = WindIssueCardVerify(userToken=self.userToken, reqSeq=self.req_seq, partnerToken='222',nonce=datetime.datetime.now().strftime('%Y%m%d'))
        issue_card_verify = WindIssueCardVerify(userToken=self.userToken, reqSeq=self.req_seq, partnerToken='222',nonce="123456")

        # issue_card_verify = WindIssueCardVerify(userToken="", reqSeq=self.req_seq, partnerToken='222',nonce='')
        # issue_card_verify = WindIssueCardVerify(userToken="", reqSeq=self.req_seq, partnerToken='222',nonce='',coBrandCard=None)
        # issue_card_verify = WindIssueCardVerify(userToken=self.userToken, reqSeq="", partnerToken='222')
        # issue_card_verify = WindIssueCardVerify(userToken="", reqSeq=self.req_seq, partnerToken='444',nonce='')

        logger.info("发起issue_card请求")
        issue_card_response = HttpUtils.http_post(
            url=issue_card_verify.url(),
            json=issue_card_verify.make_payload()
        ).json()
        error_count, error_msg_list = issue_card_verify.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True
    def test_TC002_003(self):
        """
        用例名称:
          开卡参数校验 coBrandCard和partnerNo和合作方申请令牌互相不配对
        """
        # issue_card_verify = WindIssueCardVerify(userToken=self.userToken, reqSeq=self.req_seq, partnerToken='555',partnerNo='newyork001')
        issue_card_verify = WindIssueCardVerify(userToken=self.userToken, reqSeq=self.req_seq, partnerToken='555',coBrandCard='newyorktype001')
        logger.info("发起issue_card请求")
        issue_card_response = HttpUtils.http_post(
            url=issue_card_verify.url(),
            json=issue_card_verify.make_payload()
        ).json()
        error_count, error_msg_list = issue_card_verify.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True

    def test_TC002_004(self):
        """
        用例名称:
           开卡参数校验 合作方标识，联名卡类型编码状态无效或者reqseq申请流水不为之前传入的申请流水
        """
        issue_card_verify = WindIssueCardVerify(userToken=self.userToken, reqSeq="2103300901281893001", partnerToken='55567')
        logger.info("发起issue_card请求")
        issue_card_response = HttpUtils.http_post(
            url=issue_card_verify.url(),
            json=issue_card_verify.make_payload()
        ).json()
        error_count, error_msg_list = issue_card_verify.assert_response_data(issue_card_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True




