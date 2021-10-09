# -*- coding: utf-8


import json
from common import consts,config_util
from common.config_util import getconfig, getCert
from common.string_util import *
from collections import OrderedDict
from common.crypto_util import sign_rsawithsha256_signature
from common.crypto_util import aes256_gcm_encrypt
from common.crypto_util import aes256_cbc_pkcs7padding_encrypt
import datetime


dey1='xv0EJc9XkFHaCthTJgWPvw=='
parnterData= aes256_cbc_pkcs7padding_encrypt(bytes(dey1, encoding='utf-8'),'QV5VRXX8WDUS')  #aescbc对称加密

print(parnterData)


sign_rsawithsha256_signature()