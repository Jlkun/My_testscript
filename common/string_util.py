# -*- coding: utf-8


import logging
import hashlib
import uuid
import random

logger = logging.getLogger(__name__)

def assert_equal(left, right, message=None):
    if left != right:
        logger.error('%s != %s ' % (left, right))
        if message:
            logger.error(message)
        return False
    else:
        return True


def create_key_value_string(source):
    temp = [(k, source[k]) for k in sorted(source.keys())]
    data = ''
    for i in range(0, len(temp)):
        data = data + temp[i][0] + '=' + temp[i][1]
        if i < len(temp) - 1:
            data = data + '&'
    return data


def random_app_uuid():  #定义 appUserId为01开头的10位
    list = [2, 3, 4, 5, 6, 7, 8, 9]
    slice = random.sample(list, 8)
    random_app_uuid = '01' + ''.join(str(i) for i in slice)
    return random_app_uuid

def random_card_num():  #定义 校园联名卡号为02开头的11位
    list = [0,1, 3, 4, 5, 6, 7, 8, 9]
    slice = random.sample(list, 9)
    random_card_num = '02' + ''.join(str(i) for i in slice)
    return random_card_num

def moka_random_card_num():  #定义 moka校园联名卡号为3104770003开头的1位
    list = [0,1, 3, 4, 5, 6, 7, 8, 9]
    slice = random.sample(list, 9)
    random_card_num = '3104770003' + ''.join(str(i) for i in slice)
    return random_card_num

def paetner_token():  #定义 paetner_token为ptoken开头的10位
    list = [2, 3, 4, 5, 6, 7, 8, 9]
    slice = random.sample(list, 8)
    random_app_uuid = 'ptoken' + ''.join(str(i) for i in slice)
    return random_app_uuid

def paetner_user_id():  #定义 paetner_user_id为puid开头的10位
    list = [2, 3, 4, 5, 6, 7, 8, 9]
    slice = random.sample(list, 8)
    random_app_uuid = 'puid' + ''.join(str(i) for i in slice)
    return random_app_uuid


def order_no():  #定义 paetner_user_id为000开头的10位
    list = [2, 3, 4, 5, 6, 7, 8, 9]
    slice = random.sample(list, 8)
    random_app_uuid = '000' + ''.join(str(i) for i in slice)
    return random_app_uuid