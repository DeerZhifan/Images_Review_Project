from Crypto.Cipher import DES
from binascii import b2a_hex, a2b_hex


class PassWord(object):
    def __init__(self, public_key):
        """public_key为长度为8的字符串"""
        public_key = bytes(public_key, encoding='utf-8')
        self.des = DES.new(public_key, DES.MODE_ECB)

    @staticmethod
    def pad(text):
        """将字符串的长度变为8的倍数"""
        while len(text) % 8 != 0:
            text += ' '
        return text

    def encrypt_text(self, text):
        """加密"""
        padded_text = bytes(self.pad(text), encoding='utf-8')
        encrypted_text = self.des.encrypt(padded_text)
        return b2a_hex(encrypted_text).decode()

    def decrypt_text(self, encrypted_text):
        """解密"""
        decrypted_text = self.des.decrypt(a2b_hex(encrypted_text))
        decrypted_text = decrypted_text.decode(encoding='utf-8').rstrip()
        return decrypted_text

