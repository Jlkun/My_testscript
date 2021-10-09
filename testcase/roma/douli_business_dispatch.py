# -*- coding: utf-8 -*-
# ! /usr/bin/env python
# encoding=utf-8
# Case ID      ：TC02005001
# Description  : business-
# Author       : shuyiqing
# Version      : 0.1
# Date         ：2020/9/15

import time
import json
import logging
import unittest
import datetime
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common import log, exec_remote_server, consts
from common.config_util import getconfig

config = getconfig()

logger = logging.getLogger(__name__)


class TestTC020051001(unittest.TestCase):

    # Before ervey case start
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

        logger.info("%s end at:%s" % (self._testMethodName, get_date_now()))

    def test_TC02005001_001_V0111(self):
        """
        用例名称:
            business-dispatch(兜礼线下充值券)
        """

        # self.product_code = consts.WProductCode
        self.product_code = "SPA-T-R-2C-2021-08-DOOOLY"
        self.amount = 500
        # self.bn = consts.WBN
        self.bn = "05000050888010010007" #
        business_dispatch = DouliBusinessDispatch(bn=self.bn, cardNo=self.card_no, phoneNo=self.phone_no,
                                             orderNo=self.order_no,
                                             productCode=self.product_code, amount=self.amount)
        logger.info("发起business-dispatch请求")
        business_dispatch_response = HttpUtils.http_post(
            url=business_dispatch.url(),
            json=business_dispatch.make_payload()
        ).json()
        business_dispatch_response = business_dispatch_response
        error_count, error_msg_list = business_dispatch.assert_response_data(business_dispatch_response)



        self.error_count = self.error_count + error_count
        self.res_seq = business_dispatch_response['spaAcceptSeq']
        self.accept_time = business_dispatch_response['acceptTime']
        count = self.spa_roma_session.query(RomaBusinessRecord).filter(
            RomaBusinessRecord.phone_no == self.phone_no,
            RomaProduct.out_product_code == self.product_code,
            RomaBusinessRecord.product_id == RomaProduct.id,
            RomaBusinessRecord.out_product_code == self.product_code,
            RomaBusinessRecord.card_no == self.card_no,
            RomaBusinessRecord.amount == self.amount,
            RomaBusinessRecord.third_order_no == self.order_no,
            RomaBusinessRecord.res_seq == self.res_seq,
            RomaBusinessRecord.res_date == self.accept_time,
        ).count()
        if assert_equal(count, 1) is False:
            error_msg = 'tbl_roma_business_record未找到记录'
            self.error_count += 1
            self.error_msg_list.append(error_msg)
        self.test_finish = True

