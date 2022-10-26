import base64
# from lib.exceptions import DecryptionFailureException, EncryptionFailureException
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from Crypto.Random import get_random_bytes
import hashlib
import logging

from django.conf import settings



class AESEncryption(object):
    def decrypt(self, encrypted_text):
        password = ' '
        # msg = base64.b64decode(encrypted_text)
        msg = encrypted_text
        salt = msg[:20]
        iv = msg[settings.VI_DECRYPTION_SALT_BYTE_LENGTH: settings.VI_DECRYPTION_IV_BYTE_LENGTH + settings.VI_DECRYPTION_SALT_BYTE_LENGTH]
        msg = msg[settings.VI_DECRYPTION_IV_BYTE_LENGTH + settings.VI_DECRYPTION_SALT_BYTE_LENGTH:]

        key = hashlib.pbkdf2_hmac('SHA1', password.encode(), salt, 65556, 32)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_text = unpad(cipher.decrypt(msg), AES.block_size).decode('utf-8')

        return decrypted_text