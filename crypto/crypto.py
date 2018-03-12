''' Crypto module for Papillon

Helper functions and wrappers around (hopefully) serious crypto libs, providing
convenient defaults and homogeneous cryptography '''

from hashlib import sha256
from Crypto.Cipher import AES
from Crypto import Random


class AESCipher:
    ''' AES encryption and decryption '''

    BLOCK_SIZE = 16

    def __init__(self, key):
        self.key = self._derive_key(key)

    def _pad(self, data):
        ''' Pads `data` to a multiple of `BLOCK_SIZE` '''
        pad_size = self.BLOCK_SIZE - (len(data) % self.BLOCK_SIZE)
        padding = bytes([pad_size] * pad_size)
        return data + padding

    @staticmethod
    def _unpad(data):
        ''' Removes the padding added by `_pad` '''
        pad_size = data[-1]
        return data[:-pad_size]

    @staticmethod
    def _derive_key(key):
        ''' Derives a key of the correct size from anything it gets. Returns
        the input itself whenever `key` is a 256b `bytes`, or a sha256
        otherwise. '''

        if isinstance(key, bytes):
            if len(key) == 256 // 8:
                return key
            return sha256(key).digest()
        return sha256(key.encode('utf8')).digest()

    def encrypt(self, inp):
        ''' Encode a binary blob to a binary blob '''
        padded = self._pad(inp)
        init_vector = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, init_vector)
        return init_vector + cipher.encrypt(padded)

    def decrypt(self, enc):
        ''' Decrypt a binary blob to a binary blob '''
        init_vector = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, init_vector)
        return self._unpad(cipher.decrypt(enc[16:]))
