from base64 import b64decode, b64encode
from cgi import print_arguments
from requests import request
import requests
from bs4 import BeautifulSoup
import re
import json
from Yowaimo.Parsers.constants import *
from Yowaimo.myCrypto.KdramaCrypto import KdramaCrypto


class KdramaParaser(KdramaCrypto):
    def __init__(self) -> None:
        super().__init__(KDRAMA_KEY, KDRAMA_IV)
        self.baseUrl, self.baseAjaxUrl, self.iframeReqHeaders, self.m3u8ReqHeaders = KDRAMA_BASE_URL, KDRAMA_AJAX_URL, KDRAMA_IFRAME_HEADERS, KDRAMA_M3U8_HEADERS

    # def search(self, drama):
    #     page = requests.get(f'{KDRAMA_BASE_HOST}//search.html?keyword={drama}')
    #     soup = BeautifulSoup(page.content, 'html.parser')
    #     img, name, meta = soup.find_all('div', {'class': 'picture'}), soup.find_all(
    #         'div', {'class': 'name'}), soup.find_all('div', {'class': 'meta'})
    #     searchjson = []
    #     for i in range(len(img)):
    #         searchjson.append({
    #             "drama": " ".join(name[i].getText().strip().split()[:-2]),
    #             "cover": img[i].img['src'], "meta": meta[i].getText().strip(),
    #             "episode": " ".join(name[i].getText().strip().split()[-2:])})
    #     return searchjson

    def search2(self, drama):
        page = requests.get(f'{KDRAMA_BASE_HOST}//search.html?keyword={drama}')
        soup = BeautifulSoup(page.content, 'html.parser')
        return list(
            map(lambda it: {"drama": it['alt'], "cover": it['src']},
                soup.select('#main_bg > div:nth-child(5) > div > div.vc_row.wpb_row.vc_row-fluid.vc_custom_1404913114846 > div.vc_col-sm-12.wpb_column.column_container > div > div > ul > li > a > div.img > div.picture > img')))

    # def getdramainfo(self, drama):
    #     page = requests.get(f'{KDRAMA_BASE_HOST}//videos/{drama}-episode-1')
    #     soup = BeautifulSoup(page.content, 'html.parser')
    #     dramainfo = []
    #     img, name, meta = soup.find_all('div', {'class': 'picture'}), soup.find_all(
    #         'div', {'class': 'name'}), soup.find_all('div', {'class': 'meta'})
    #     info = soup.find('div', {'class': 'content-more-js'})
    #     total_episodes = int(name[0].getText().strip().split()[-1])
    #     episode_thumbnails = []
    #     latest_episodes = []
    #     for i in range(total_episodes):
    #         episode_thumbnails.append(img[i].img['src'])
    #     for i in range(total_episodes, len(name)):
    #         latest_episodes.append({
    #             "drama": " ".join(name[i].getText().strip().split()[:-2]),
    #             "cover": img[i].img['src'], "meta": meta[i].getText().strip(),
    #             "episode": " ".join(name[i].getText().strip().split()[-2:])})
    #     dramainfo.append({
    #         "summary": info.getText()[1:],
    #         "total_episodes": total_episodes,
    #         "episode_thumbnails": episode_thumbnails})
    #     return dramainfo

    def getdramainfo2(self, drama):
        page = requests.get(f'{KDRAMA_BASE_HOST}//videos/{drama}-episode-1')
        soup = BeautifulSoup(page.content, 'html.parser')
        dramainfo = []
        total_episodes = len(soup.select(
            '#main_bg > div:nth-child(5) > div > div.video-info-left > ul > li'))
        info = soup.find('div', {'class': 'content-more-js'})
        dramainfo.append({
            "summary": info.getText()[1:],
            "total_episodes": total_episodes})
        return dramainfo

    # def homepage(self):
    #     page = requests.get(KDRAMA_BASE_HOST)
    #     soup = BeautifulSoup(page.content, 'html.parser')
    #     img, name = soup.find_all('div', {'class': 'picture'}), soup.find_all(
    #         'div', {'class': 'name'})
    #     homejson = []
    #     for i in range(len(img)):
    #         homejson.append({
    #             "drama": " ".join(name[i].getText().strip().split()[:-2]),
    #             "cover": img[i].img['src'],
    #             "episode": " ".join(name[i].getText().strip().split()[-2:])})
    #     return homejson

    def homepage2(self):
        page = requests.get(KDRAMA_BASE_HOST)
        soup = BeautifulSoup(page.content, 'html.parser')
        return list(
            map(lambda it: {'drama': it['alt'], 'cover': it['src']},
                soup.select('#main_bg > div:nth-child(5) > div > div.vc_row.wpb_row.vc_row-fluid.vc_custom_1404913114846 > div.vc_col-sm-12.wpb_column.column_container > div > div > ul > li > a > div.img > div.picture > img')))

    def getIframeUrl(self, url):
        data = request("GET", url).text
        surl = re.findall(r'//dembed.*\" all', data)
        return surl[0][:-5]

    def getMsgFromIframe(self, url):
        response = request("GET", url, headers=self.iframeReqHeaders, data={})
        data = response.text
        msg = re.findall(r'data-value.*><', data)[0]
        msg = msg[11:-2]
        return msg

    def makeM3u8ReqUrl(self, msg):
        print(msg)
        new_url = self._decrypt(msg)
        print(new_url)
        print(type(new_url))
        id_msg = new_url[:8].decode("utf-8")
        new_id = self._encrypt(id_msg)
        return self.baseAjaxUrl+"?id="+new_id+new_url[8:].decode("utf-8")+"&alias="+id_msg

    def getM3u8(self, url):
        response = request("GET", url, headers=self.m3u8ReqHeaders, data={})
        data = json.loads(response.text)['data']
        return self._decrypt(data).decode("utf-8")

    def getVidLink(self, drama, episode):
        try:
            print(drama,episode)
            url = self.getIframeUrl(KDRAMA_BASE_URL+drama+"-episode-"+episode)
            msg = self.getMsgFromIframe("https:"+url)
            final_url = self.makeM3u8ReqUrl(msg)
            res = self.getM3u8(final_url)
            out = json.loads(res)
            return out['source'][0]['file']
        except:
            return json.dumps({"eror": "error occured while scrapping"})
