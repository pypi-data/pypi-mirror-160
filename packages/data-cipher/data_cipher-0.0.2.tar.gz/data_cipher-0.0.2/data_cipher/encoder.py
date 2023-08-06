import hashlib
from base64 import b64decode, b64encode
from typing import Union
from struct import pack

from Crypto import Random
from Crypto.Cipher import AES, Blowfish


class Encoder(object):

    def __init__(self):
        self.block_size = AES.block_size

    def __pad(self, plain_text: str) -> str:
        number_of_bytes_to_pad = self.block_size - \
            len(plain_text) % self.block_size
        ascii_string = chr(number_of_bytes_to_pad)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str
        return padded_plain_text

    def __unpad(self, plain_text: str) -> str:
        last_character = plain_text[len(plain_text) - 1:]
        return plain_text[:-ord(last_character)]

    def aes_encrypt(self, plain_text: str, key: str) -> str:
        """
        AES algo encryption
        Algorithm - AES
        One of the best ways to encrypt data, 
        in this case using 256 bit form

        Args:
            plain_text (str): source text to encrypt
            key (str): the key with which the message will be decrypted

        Returns:
            str: encrypted text
        """
        plain_text = self.__pad(plain_text)
        iv = Random.new().read(self.block_size)
        cipher = AES.new(hashlib.sha256(
            key.encode()).digest(), AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(plain_text.encode())
        return b64encode(iv + encrypted_text).decode("utf-8")

    def aes_decrypt(self, encrypted_text: str, key: str) -> str:
        """
        AES algo decryption

        Args:
            encrypted_text (str): encrypted text
            key (str): key used for encryption

        Returns:
            str: source text
        """
        encrypted_text = b64decode(encrypted_text)
        iv = encrypted_text[:self.block_size]
        cipher = AES.new(hashlib.sha256(
            key.encode()).digest(), AES.MODE_CBC, iv)
        plain_text = cipher.decrypt(
            encrypted_text[self.block_size:]).decode("utf-8")
        return self.__unpad(plain_text)

    def blowfish_encrypt(self, plain_text: str, key: str) -> str:
        """
        Blowfish algo encryption

        Args:
            plain_text (str): source text to encrypt
            key (str): the key with which the message will be decrypted

        Returns:
            str: encrypted text
        """
        bs = Blowfish.block_size
        cipher = Blowfish.new(key.encode("utf-8"), Blowfish.MODE_CBC)
        plen = bs - len(plain_text) % bs
        padding = [plen]*plen
        padding = pack('b'*plen, *padding)
        encrypted = cipher.iv + \
            cipher.encrypt(
                (plain_text + padding.decode("utf-8")).encode("utf-8"))
        return encrypted

    def blowfish_decrypt(self, encrypted_text: str, key: str) -> str:
        """
        Blowfish algo decryption

        Args:
            encrypted_text (str): encrypted text
            key (str): key used for encryption

        Returns:
            str: source text
        """
        bs = Blowfish.block_size
        iv = encrypted_text[:bs]
        ciphertext = encrypted_text[bs:]
        cipher = Blowfish.new(key.encode("utf-8"), Blowfish.MODE_CBC, iv)
        msg = cipher.decrypt(ciphertext)
        last_byte = msg[-1]
        msg = msg[:- (last_byte if type(last_byte) is int else ord(last_byte))]
        return repr(msg)
