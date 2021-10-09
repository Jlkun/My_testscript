# -*- coding: utf-8

from common.models_wind import *
from common.string_util import *
from common import consts,config_util,log,exec_remote_server
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from interface.issue_card import WindIssueCard
from interface.reset_face import ResetFace
from interface.reset_face_new import ResetFaceNew
from interface.get_partner_card_list import GetPartnerCardList
from interface.issuecardconfirm import IssueCardFirm
from interface.notify_bind_result import NotifyBindResult
from interface.get_token import GetToken
from common.http_utils import HttpUtils
import unittest
import logging
config = config_util.getconfig()

class TestTC02010001(unittest.TestCase):
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
        self.userToken ='3abf9ea72c9c45369e637314a51032db'


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

    def test_TC01011FF_001(self):
        """
        用例名称:
           合作方向复旦微wind进行换卡面
        """

        Reset_Face_New = ResetFaceNew(cardNo='3104770002054731968',skinId='123456789')
        # Reset_Face_New = ResetFaceNew(cardNo='3104770002054731968')
        logger.info("发起issue_card请求")
        Reset_Face_New_response=HttpUtils.http_post(
            url=Reset_Face_New.url(),
            json=Reset_Face_New.make_payload()
        ).json()
        error_count, error_msg_list = Reset_Face_New_response.assert_response_data(Reset_Face_New_response)
        self.error_count = self.error_count + error_count
        self.error_msg_list.extend(error_msg_list)
        self.test_finish = True
