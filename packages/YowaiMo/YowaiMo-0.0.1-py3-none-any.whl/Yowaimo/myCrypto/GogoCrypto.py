from Yowaimo.myCrypto.BaseCrypto import *

class GogoCrypto(BaseCrypto):
    def __init__(self,key,iv) -> None:
        super().__init__(key,iv)

    
    def _decryptGogom3u8(self,msg,key):
        try:
            iv = self.iv.encode("utf8")
            ct = b64decode(msg)
            cipher = AES.new(key.encode("utf8"), AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return pt
        except (ValueError, KeyError):
            return ValueError
