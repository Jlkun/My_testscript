# -*- coding: utf-8

import random
import uuid
from mock import issue_card_confirm_mock
from mock.issue_card_confirm_mock import IssueCardConfirm
from mock.query_card_mock import QueryCard
from common import thread_utils
from common import consts,config_util,log,exec_remote_server
import logging
# class test:
#     def aaa(self):
#         print(111)
#     def bbb(self):
#         self.aaa()
#     pass

# logger = logging.getLogger(__name__)
log.setLog()
# issue_card_confirm.IssueCardConfirm().set_response(user_phone=self.phone_no, user_status=consts.AppUserStatus.UNEXIST)

print(111)
# QueryCard(fpanMainStatus=1,fpanStatus=4)
# IssueCardConfirm().set_response()
mock_thread = thread_utils.MockServerThread(timeount=60000)
mock_thread.start()
print(222)


# tt=test()
# tt.bbb()

# test().bbb()

# num = random.randint(1, 50)
# print(num)

# print(random.choice(['Jason', 'is', 'so', 'handsome']))
# print(uuid.uuid4().hex)

# list = [ 2,3, 4, 5, 6, 7, 8, 9]
# slice = random.sample(list, 8)
# str = '01'+''.join(str(i) for i in slice)
# print(str)
#
#
# print(slice)



