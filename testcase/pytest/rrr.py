# -*- coding: utf-8
import codecs

# str="wToG+4mlRNcOZRvox4DN2V7P52I/6Wm8BWreRhD5qoWDVW7HPVLi0z0Jm"
# list=[]
# print([])
# print(list)
# from common.crypto_util import aes256_cbc_pkcs7padding_encrypt
# key='eW4SMc2G80wcWEHLmEzAKg0hx298vrDo'
# print(aes256_cbc_pkcs7padding_encrypt(bytes(key, encoding='utf-8'),'This is java bcprovlib pkcs7padding PKCS7 TEST'))
from common import consts
import datetime
import logging
import json
from common import consts,config_util
from common.config_util import getconfig, getCert
from common.string_util import *
from collections import OrderedDict
from common.crypto_util import sign_rsawithsha256_signature
from common.crypto_util import aes256_gcm_encrypt
from common.crypto_util import aes256_cbc_pkcs7padding_encrypt
import datetime
config = config_util.getconfig()
logger = logging.getLogger(__name__)

sign_source = OrderedDict()
sign_source['userId'] = '11321'

rsa_pri_key_file_name = config.get('keys', 'aliver_1711_fmsh_test_rsa2048pri_key')
rsa_pri_key_file_name = config.get('keys', 'aliver_1711_fmsh_test_rsa2048pri_key1')
with open(getCert(rsa_pri_key_file_name), "r") as f:
    # rsa_pri_key = f.read()
    # print (type(rsa_pri_key))
    str='MIICXQIBAAKBgQDgXv9YZLhYf8hryEFvwGhzglevAMMdPSg1NSQ1UdqEPa0uzOWKZhOryAuwoQev9OOrty67ieGmNVuLoKyQwNXM+dEPp0qXGjP5rTuK3Jdr9Kqi4xWgr/Q/WD2FnIakI//xFgYVUKpcakEzmhYTpk8ZWUjOlR9SjZA2MJS32sYSLwIDAQABAoGBAL0Oju42gDbiBUj8hlbZs6mQ7L1jUQT0IUskKgxbmlrPdXv33nqNpImcmG0OYuHa4XQxeElB10crsqWmj4GxWvQ2nkEfCDL+nskV7lG1UocaOhro3+LtV7rY9xAftxHtRNb6pKowT8HQmShiCnFhGznc/ebMaqdFARCgBvvxUyChAkEA9BXlpT/vqOv+ey0DzTJ9DTmzbnY5vwqbgUVDvEFH+CHR9KkEBENl5Yj7tVQhaOGBtMjHp2EhgUdZRgMap5Z+6QJBAOtSv27341oq/Xa5uKfr3v/pqm7HH3Noh/mjDg/3118nrC6+hKlJOAfHhXRtcmw/SP/RXk2rjpdniQyKwM+cyVcCQADcPuX5NrgKtOfsPbIwdl5gkLBX/FYfDHNFMjrso/tM6zeIjPoS3r4TYIfAFyoOeW2Qs5t0bTDOdpMXmbVzg1kCQFbASpI+EDJNZuM91DUTX0I4gfwUrCN/haEh2y1H0L3jgjY5Re6ib2VuyGQDdQsyyVaFeJ5pgEeQg5V8EVh4FEECQQCxkMTXn0br9zgrSnsSuqyp0T+rzZPhFk4LaipH2SX4c7iIiHasd2wb7kv9YzmQvr2VvLI7evzdzPE4d/Xi6XNH'


    logger.info(
        ' business-dispcath sign_source:%s' % json.dumps(sign_source).replace('\\', '').replace(' ', ''))
    print( ' business-dispcath sign_source:%s' % json.dumps(sign_source).replace('\\', '').replace(' ', ''))
#
sign = sign_rsawithsha256_signature(str,
                                    json.dumps(sign_source).replace('\\', '').replace(' ', '')).upper()





# str1=''
# list=[bytes.decode(codecs.encode(bytes(i, encoding="utf8"), "hex")).upper() for i in str]
#
#
# print(str1.join(list))


#
# class aa:
#     def __init__(self,**kwargs):
#         cc=dict()
#         cc['a']='1'
#         cc['b']='2'
#         return cc
#
#
#     def bb(self):
#         print(aa())
#
#
#
#
# aa().bb()







# dd = {
#     "resData": {
#         "bizOrderId": "548aa63f64904be6989ee4c6c6ade94f",
#         "amount": 1000,
#         "paymentExprieTime": "20201218134928",
#         "payInfo": "1608270269014",
#         "mallGoodsCode": "002",
#     },
#     "resCode": "9000",
#     "resDesc": "success"
# }
#
#
# print(dd.get('resData').get('bizOrderId'))
# print(dd.get('resData').get('bizOrderId'))



# import base64
# from Crypto.Cipher import AES
# from  hashlib import md5
# import random
#
#
# def pkcs7padding(text):
#     """
#     明文使用PKCS7填充
#     最终调用AES加密方法时，传入的是一个byte数组，要求是16的整数倍，因此需要对明文进行处理
#     :param text: 待加密内容(明文)
#     :return:
#     """
#     bs = AES.block_size  # 16
#     length = len(text)
#     bytes_length = len(bytes(text, encoding='utf-8'))
#     # tips：utf-8编码时，英文占1个byte，而中文占3个byte
#     padding_size = length if(bytes_length == length) else bytes_length
#     padding = bs - padding_size % bs
#     # tips：chr(padding)看与其它语言的约定，有的会使用'\0'
#     padding_text = chr(padding) * padding
#     return text + padding_text
#
#
# def pkcs7unpadding(text):
#     """
#     处理使用PKCS7填充过的数据
#     :param text: 解密后的字符串
#     :return:
#     """
#     length = len(text)
#     unpadding = ord(text[length-1])
#     return text[0:length-unpadding]
#
#
# def encrypt(key, content):
#     """
#     AES加密
#     key,iv使用同一个
#     模式cbc
#     填充pkcs7
#     :param key: 密钥
#     :param content: 加密内容
#     :return:
#     """
#     key_bytes = bytes(key, encoding='utf-8')
#     cipher = AES.new(key_bytes, AES.MODE_CBC, b"1234567890123456")
#     # 处理明文
#     content_padding = pkcs7padding(content)
#     # 加密
#     encrypt_bytes = cipher.encrypt(bytes(content_padding, encoding='utf-8'))
#     # 重新编码
#     result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
#     return result
#
#
# def decrypt(key, content):
#     """
#     AES解密
#      key,iv使用同一个
#     模式cbc
#     去填充pkcs7
#     :param key:
#     :param content:
#     :return:
#     """
#     key_bytes = bytes(key, encoding='utf-8')
#     cipher = AES.new(key_bytes, AES.MODE_CBC, b"1234567890123456")
#     # base64解码
#     encrypt_bytes = base64.b64decode(content)
#     # 解密
#     decrypt_bytes = cipher.decrypt(encrypt_bytes)
#     # 重新编码
#     result = str(decrypt_bytes, encoding='utf-8')
#     # 去除填充内容
#     result = pkcs7unpadding(result)
#     return result
#
#
# def get_key(n):
#     """
#     获取密钥 n 密钥长度
#     :return:
#     """
#     c_length = int(n)
#     source = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
#     length = len(source) - 1
#     result = ''
#     for i in range(c_length):
#         result += source[random.randint(0, length)]
#     return result
#
#
# # Test
# # 非16字节的情况
# aes_key = "dm2GWcnZn3e7BbENi4GkQmdba3fMDPKP"
# source_en = 'hello'
# encrypt_en = encrypt(aes_key, source_en)
# print(encrypt_en)














# # -*- coding=utf-8-*-
# from Crypto.Cipher import AES
# import os
# from Crypto import Random
# import base64
#
# """
# aes加密算法
# padding : PKCS7
# """
#
# class AESUtil:
#
#     __BLOCK_SIZE_16 = BLOCK_SIZE_16 = AES.block_size
#
#     @staticmethod
#     def encryt(str, key, iv):
#         cipher = AES.new(key, AES.MODE_CBC,iv)
#         x = AESUtil.__BLOCK_SIZE_16 - (len(str) % AESUtil.__BLOCK_SIZE_16)
#         if x != 0:
#             str = str + chr(x)*x
#         msg = cipher.encrypt(str)
#         # msg = base64.urlsafe_b64encode(msg).replace('=', '')
#         msg = base64.b64encode(msg)
#         return msg
#
#     @staticmethod
#     def decrypt(enStr, key, iv):
#         cipher = AES.new(key, AES.MODE_CBC, iv)
#         # enStr += (len(enStr) % 4)*"="
#         # decryptByts = base64.urlsafe_b64decode(enStr)
#         decryptByts = base64.b64decode(enStr)
#         msg = cipher.decrypt(decryptByts)
#         paddingLen = ord(msg[len(msg)-1])
#         return msg[0:-paddingLen]
#
# if __name__ == "__main__":
#     key = "1234567812345678"
#     iv = "1234567812345678"
#     res = AESUtil.encryt("123456", key.encode('utf-8'), iv)
#     print (res )# 2eDiseYiSX62qk/WS/ZDmg==
#     # print (AESUtil.decrypt(res, key, iv)) # 123456

