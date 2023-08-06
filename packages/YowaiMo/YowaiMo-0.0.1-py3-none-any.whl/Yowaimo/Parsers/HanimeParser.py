from base64 import b64decode, b64encode
from requests import request
import json


class HanimeParser:
    def __init__(self,hanime="",ep = 1) -> None:
        self.hanime,self.ep = hanime,ep

    def search(self,key):
        url = "https://search.htv-services.com/"
        payload = {"search_text":key,"tags":[],"tags_mode":"AND","brands":[],"blacklist":[],"order_by":"created_at_unix","ordering":"desc","page":0}
        headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Mobile Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Sec-GPC': '1',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'host': 'search.htv-services.com'
        }
        response = request("POST", url, headers=headers, data=json.dumps(payload))
        return response.text

    def getHanimeEp(self):
        url = 'https://hanime.tv/api/v8/video?id={}-{}'.format(self.hanime,self.ep)
        print(url)
        res = request('GET',url).text
        res = json.loads(res)
        # m3u8 = res['videos_manifest']['servers'][0]['streams'][1]['url']
        return res
