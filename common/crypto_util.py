# -*- coding: utf-8 -*-

from binascii import b2a_hex, a2b_hex
import base64
import hashlib
import hmac
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, SHA1
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
import json
MODE_ECB = 1
MODE_CBC = 2
NO_PADDING = 0
PKCS7_PADDING = 1
NIST_PADDING = 2
ZERO_PADDING = 3

def aes256_gcm_encrypt(key, data, iv=b'\x00'*12):
    """
    AES 256 GCM Encryption

    :param key: AES key
    :param data: Data to be encrypted.
    :param iv: Initial value
    :return: Cryptogram
    """
    a = key.hex()
    cipher = AES.new(key, AES.MODE_GCM, iv)

    cipher.update(b'')

    encrypted, new_tag = cipher.encrypt_and_digest(data)
    return encrypted + new_tag

def aes256_gcm_decrypt(key, data, tlen=16, iv=b'\x00' * 12):
    """
    AES 256 GCM Decryption

    :param tlen:
    :param key: AES Key
    :param data: Data to be decrypted
    :param iv: Initial value.
    :return: Plain text
    """
    cipher = AES.new(key, AES.MODE_GCM, iv)
    cipher.update(b'')
    decrypted_data = cipher.decrypt_and_verify(data[:-tlen], data[-tlen:])
    return decrypted_data

def unpad_with_scheme(data, scheme):
    """
    Unpad the data with the specified scheme.

    :param data: Data to be unpadded.
    :param scheme: See the scheme param in the pad_with_scheme.
    :return: Data after unpadding.
    """
    if scheme == NO_PADDING:
        pass
    elif scheme == PKCS7_PADDING:
        strip_number = ord(data[-1])
        data = data[:-strip_number]
    elif scheme == NIST_PADDING:
        for i in range(-1, -len(data)-1, -1):
            if data[i] == '\x80':
                data = data[:i]
                break
    return data


def pad_with_scheme(data, scheme, block_size):
    """
    Pad the data with the specified scheme

    :param data: Data to be padded
    :param scheme:
        NO_PADDING(0)   : Do NOT pad.
        PKCS7_PADDING(1): Padding with byte n until reaching multiple of block size.
        NIST_PADDING(2) : Padding with first byte 80 and then 00 until reaching
                          multiple of block size.
        ZERO_PADDING(3) : Padding with 0 until reaching the multiple of block size.
        e.g. for block size 8, given a data 12345678,
            After PKCS7_PADDING, it will be 1234567804040404
            After NIST_PADDING, it will be 1234567880000000
            After ZERO_PADDING, it will be 1234567800000000
        Note: If the data is already a mutiple of block size, still padding
              block_size bytes.
    :param block_size: Block size.
    :return: Data after padding.
    """
    padding_number = block_size - len(data) % block_size
    if scheme == NO_PADDING:
        pass
    elif scheme == PKCS7_PADDING:
        data += (block_size - len(data) % block_size) * chr(block_size - len(data) % block_size)
    elif scheme == NIST_PADDING:
        data += '\x80' + '\x00' * (padding_number - 1)
    elif scheme == ZERO_PADDING:
        data += '\x00' * padding_number
    return data


def aes_encrypt_b64(key, data, mode, padding=0, iv=b'\0'*16):
    """
    AES encryption.

    :param key: AES key. 128 bits or 256 bits.
    :param data: Data to be encrypted.
    :param mode: MODE_ECB or MODE_CBC supported.
    :param padding: See the scheme param in the pad_with_scheme.
    :param iv: Initial vector. Default set to 00 of 16 bytes.
    :return: AES cryptogram.
    """
    if mode == MODE_CBC:
        cipher = AES.new(key, mode, iv)
    else:
        cipher = AES.new(key, mode)
    data = pad_with_scheme(data, padding, block_size=AES.block_size)
    return str(base64.b64encode(cipher.encrypt(data.encode('utf-8'))), 'utf-8')


def aes_decrypt(key, data, mode, padding=0, iv=b'\0'*16):
    """
    AES decryption.

    :param key: AES key. 128 bits or 256 bits.
    :param data: Data to be encrypted.
    :param mode: MODE_ECB or MODE_CBC supported.
    :param padding: See the scheme param in the pad_with_scheme.
    :param iv: Initial vector. Default set to 00 of 16 bytes.
    :return: AES plain text.
    """
    if mode == MODE_CBC:
        cipher = AES.new(key, mode, iv)
    else:
        cipher = AES.new(key, mode)
    return unpad_with_scheme(cipher.decrypt(data).decode('utf-8'), padding)


def rsa_encrypt_b64(key, data):
    # RSA加密&BASE64编码
    pub_key = RSA.importKey(key)
    cipher_rsa = PKCS1_v1_5.new(pub_key)
    plain_text = data.encode()
    en_data = cipher_rsa.encrypt(plain_text)
    return str(base64.b64encode(en_data), 'utf-8')


def rsa_decrypt_b64(key, data, password=None, length=128):
    """
    1024bit的证书用128，2048bit证书用256位
    """
    en_data = base64.b64decode(data)
    pri_key = RSA.importKey(key, password)
    cipher_rsa = PKCS1_v1_5.new(pri_key)
    plain_text = cipher_rsa.decrypt(en_data, None)
    return str(plain_text, 'utf-8')


def rsa_decrypt(key, data, password=None):
    """
    1024bit的证书用128，2048bit证书用256位
    """
    pri_key = RSA.importKey(key, password)
    cipher_rsa = PKCS1_v1_5.new(pri_key)
    plain_text = cipher_rsa.decrypt(data, None)
    return str(plain_text, 'utf-8', "ignore")


def aes256_cbc_pkcs7padding_encrypt(key, data, iv=b'\0'*16):
    """
    Encrypt the plain text with AES256/CBC/PKCS7Padding.

    :param key: AES key
    :param data: Data to be encrypted.
    :param iv: Initival vector. Default set to 00 of 16 bytes.
    :return: AES cryptogram.
    """
    return aes_encrypt_b64(
        key=key,
        data=data,
        mode=MODE_CBC,
        padding=PKCS7_PADDING,
        iv=iv
    )


def sign_rsawithsha256_signature(key, source):
    signer_pri_obj = Signature_pkcs1_v1_5.new(RSA.importKey(key))
    rand_hash = SHA256.new()
    rand_hash.update(source.encode())
    signature = signer_pri_obj.sign(rand_hash)
    return b2a_hex(signature).decode('utf-8')


def verify_rsawithsha256_signature(key, signature, source):
    """
    Verify the RSAwithSHA256 signature

    :param signature: Signature to be verified.
    :param key: Private key used to sign.
    :param source: Source message.
    :return: Signature.
    """
    signature = a2b_hex(signature.encode("utf-8"))
    pubkey = RSA.importKey(key)
    digest = SHA256.new()
    digest.update(source.encode())
    signer = Signature_pkcs1_v1_5.new(pubkey)
    return signer.verify(digest, signature)


def sign_rsawithsha1_signature(key, source):
    signer_pri_obj = Signature_pkcs1_v1_5.new(RSA.importKey(key))
    rand_hash = SHA1.new()
    rand_hash.update(source.encode())
    signature = signer_pri_obj.sign(rand_hash)
    return b2a_hex(signature).decode('utf-8')


def verify_rsawithsha1_signature(key, signature, source):
    """
    Verify the RSAwithSHA1 signature

    :param signature: Signature to be verified.
    :param key: Private key used to sign.
    :param source: Source message.
    :return: Signature.
    """
    signature = a2b_hex(signature.encode("utf-8"))
    pubkey = RSA.importKey(key)
    digest = SHA1.new()
    digest.update(source.encode())
    signer = Signature_pkcs1_v1_5.new(pubkey)
    return signer.verify(digest, signature)


def md5(source):
    m = hashlib.md5()
    m.update(source.encode('utf-8'))
    return m.hexdigest()


def sign_hmac_sha256(sign_source, key):
    signature = hmac.new(bytes(key, encoding='utf-8'), bytes(sign_source, encoding='utf-8'), digestmod=hashlib.sha256).digest()
    return signature.hex().upper()

if __name__ == '__main__':
    data='v3BqL84pvuohuwSF9OJlTK9BpaZZrlNG4c3xNe/LPutuBet0zHbmhlj5Bc6JWdqwy/Ly4jaqpEjDGOnNxY4Trg7aGOeB1HLkzUbXTBXXKC4L1KU05nXcH16R+dbaQHTpvATDmDbAqKHvhxOrh5KBzYHGkhsus60oyqzOZz1eXyk+ny1L4CrvZgjVmkhnykMygA=='
    data='AAAAAAAAAAAAAAAA0ISr1nNPaNNSrj1npXycfVL8bBBfokk6BeofGxSwIreizfH1sa4w3mUF4he3OmVA1QMFB3DjR4dd4e351AQp4JiwlfuYzFZfDgHZ71ywNTN8AUpO33kt9POtwTg2Xft43CUridkdy3miaLPW6d18HV2BqZdfAsVp1za3IMJsfYcmcWRKm6KcM5ptRYA='
    key='ZiBFfN/65UCZr3s0No0UFvqdvqIU0GcffDF03rC4K8w='
    data = base64.b64decode(data)
    print(data)
    key = base64.b64decode(key)
    iv = data[:12]
    print(iv)
    data = data[12:]
    print(data)
    result = aes256_gcm_decrypt(key=key, data=data, iv=iv)
    print(result.decode())

    data={"marketUserId": "1", "appUserId": "0000670723", "channelType": "sptcc_alipay_miniPro","channelUserId": "2088512512485353"}
    data=bytes(json.dumps(data), encoding='utf-8')
    key='ZiBFfN/65UCZr3s0No0UFvqdvqIU0GcffDF03rC4K8w='
    key = base64.b64decode(key)
    iv = b'\x00' * 12
    result2=str(base64.b64encode(aes256_gcm_encrypt(key, data)),'utf-8')
    result1=str(base64.b64encode(iv),'utf-8')
    result=result1+result2
    print(result)





