# -*- coding: utf-8
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

class IssueCardConfirm:
    def __init__(self,**kwargs):
        self._url_scheme = '/issue_card_confirm'
        self._log = []
        self._return_code='0000'
        self._return_msg= 'success'
        self._userId= kwargs.get('userId', 'puid54698273')
        # self._coBrandCard= kwargs.get('coBrandCard', consts.COBRANDCARD)
        self._coBrandCard= kwargs.get('coBrandCard', "0170000506000049")
        # self._subCoBrandCard=  kwargs.get('subCoBrandCard', consts.COBRANDCARD)
        self._subCoBrandCard=  kwargs.get('subCoBrandCard', "0170000506000049")
        dey='4D494942496A414E42676B71686B6947397730424151454641414F43415138414D49494243674B43415145417258464468346A6E4358754E62685652554159444A2F7451796E526D4B4C2F54615968505532767136756C3371506C7843416C474B4B746479564A42636D72482B4D432B42795075494F354D565678324347487831585775486149766B656944337658586E5A7A4C374E6837665434376259423979627248344B6151314279692B7146576D6F425379683639537657344C574D357937326D374453736F4953654435464A6B586D336A45755262706A62536C7461306445436F504C4F67454634487748313636676E46452B586177384669326270674D4A4D3372647753745968454B69366F693079413978702F566D775A302B536A7964774F71584744796F387468305632504D72343965566D344C4135535641374F2B6E66754252594E696D526A47592F4F6F7247486B76716C544233506A612F6B4D653369612B4B583975664834634E55536A6B5A33472F5A744D653875636D77494441514142'
        dey='905799765a47929fb29fbde5e62b5f32450f120159d7adf0b373ae17fdf0a66bc345c8a9057766584d1ab8d9c235eae79515f2f4c5d584a5acd9de4074098b53efba30ea6cfe32ce983b3f53dfe062b6f02b9fd77cb59566d8d552189f67d69b248259da50b27214f4c6d965f0c9961baa6590c18f031cae100086eccbf224f1a5e4994ff549123a64fb2b1d4c58400f4a5371c2c6b9af598bd8308e05f32051bbfe710db1458c4f78ce9d6667dc04462c4d5394c7941aadc361415bb4072897dd6ec0987f33de291e17c4de92190df54d91704c00f0a45c3f54abe610c8bfb5f8966565c1f09a37822e22b0f426e13b7d197b508723372de99659b60116ed89'
        dey='5EE9C89D681C55C7472FB4FFD07E3234C1E018BD3D6227BD672DFC5931CACEDEE854F8B10982AF33F246335AD0004B02D6E2179DB47048C3B2AEDE8C1AE550ED5BE47FB8D0C0B8D5F71C901459168ADD881238BE85DA4B4690299553126F1FE048A9310488E0AE9D052A690562C8479D881DFC6EF0BAFB8E40BE508671A52817867BB4A1FDE3BE5BEDF6C8E2BDAB44460F8B390FE417B61C75CE9AC01645AB504F75CBBD23393EE71A20FF3CCC4F83EF2E5680CC4AD255039EBD446A72068960DF6F438E97F106B1647C646CD94416FB3505CB96E604D2777B197784B2249D918FF4E9CF2063D4C7D4C5EE950B28495CE89626DBE16F61D88C8FEBF8F0D5CE7C'
        self._deKey= kwargs.get('deKey', dey)
        dey1='eW4SMc2G80wcWEHLmEzAKg0hx298vrDo'
        # self._parnterData= aes256_cbc_pkcs7padding_encrypt(bytes(dey1, encoding='utf-8'),'This is java bcprovlib pkcs7padding PKCS7 TEST')  #aescbc对称加密
        self._partnerData= '00FD6D2DCE5F7177C6D2A8B9B62F057EE6271DA6653812F8B8ACF1C8B942E2C614D47F6CF5EFD96E666E9270A52D5096'
        self._extraData=  kwargs.get('extraData', 'javapythonphp')
        self._nonce=  kwargs.get('nonce', '202104291520')
        self._keyIndex=  kwargs.get('keyIndex','0')


    def make_sign(self):
        sign_source = OrderedDict()
        sign_source['userId'] = self._userId
        sign_source['coBrandCard'] = self._coBrandCard
        sign_source['subCoBrandCard'] = self._subCoBrandCard
        sign_source['deKey'] = self._deKey
        sign_source['partnerData'] = self._partnerData
        sign_source['extraData'] = self._extraData
        sign_source['nonce'] = self._nonce
        sign_source['keyIndex'] = self._keyIndex
        rsa_pri_key_file_name = config.get('keys', 'aliver_1711_fmsh_test_rsa2048pri_key')  #这里是用的合作方私钥签名
        with open(getCert(rsa_pri_key_file_name), "r") as f:
            rsa_pri_key = f.read()
            logger.info(
                ' business-dispcath sign_source:%s' % json.dumps(sign_source).replace('\\', '').replace(' ', ''))
        sign = sign_rsawithsha256_signature(rsa_pri_key,
                                            json.dumps(sign_source).replace('\\', '').replace(' ', '')).upper()
        return sign


    def get_url_scheme(self):
        return self._url_scheme

    def mock_response(self, received_url=None, received_request=None):
        logger.info('issue_card_confirm Mock收到请求')
        response = dict()
        resData = dict()
        response['resCode'] = self._return_code
        response['resDesc'] = self._return_msg
        response['resData'] =resData
        resData['userId'] =  self._userId
        resData['coBrandCard'] =  self._coBrandCard
        resData['subCoBrandCard'] =  self._subCoBrandCard
        resData['deKey'] =  self._deKey
        resData['extraData'] =  self._extraData
        resData['partnerData'] =  self._partnerData
        resData['nonce'] =  self._nonce
        resData['keyIndex'] =  self._keyIndex
        resData['sign'] = self.make_sign()
        # return  json.dumps(response)
        return  (response)
