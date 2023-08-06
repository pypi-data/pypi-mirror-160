from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

class BaseCrypto:
    def __init__(self,key,iv) -> None:
        self.key,self.iv = key,iv

    def _encrypt(self,msg):
        try:        
            cipher = AES.new(self.key.encode("utf8"), AES.MODE_CBC, self.iv.encode("utf8"))
            ct_bytes = cipher.encrypt(pad(msg.encode("utf8"), AES.block_size))
            ct = b64encode(ct_bytes).decode("utf8")
            return ct
        except ValueError as e:
            return e

    def _decrypt(self,msg):
        try:
            iv = self.iv.encode("utf8")
            ct = b64decode(msg)
            cipher = AES.new(self.key.encode("utf8"), AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return pt
        except (ValueError, KeyError):
            return ValueError