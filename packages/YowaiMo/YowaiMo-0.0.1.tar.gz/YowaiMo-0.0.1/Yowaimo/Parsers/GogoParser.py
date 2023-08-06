from base64 import b64decode, b64encode
from select import select
from requests import request
import requests
from bs4 import BeautifulSoup
import re,json
from Yowaimo.Parsers.constants import *
from Yowaimo.myCrypto.GogoCrypto import GogoCrypto

class GogoParser(GogoCrypto):
    def __init__(self) -> None:
        super().__init__(KEY, IV)
        self.baseUrl, self.baseAjaxUrl, self.iframeReqHeaders, self.m3u8ReqHeaders = BASE_URL, AJAX_URL, GOGO_IFRAME_HEADERS, GOGO_M3U8_HEADERS

    def getIframeUrl(self, url):
        data = request("GET", url).text
        surl = re.findall(r'goload.* s', data)
        return surl[0][:-3]

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
        return self._decryptGogom3u8(data, KEY2).decode("utf-8")

    def getVidLink(self, anime, episode):
        try:
            url = self.getIframeUrl(BASE_URL+anime+"-episode-"+episode)
            if 'm3u8' in url:
                return url
            msg = self.getMsgFromIframe("https://"+url)
            final_url = self.makeM3u8ReqUrl(msg)
            res = self.getM3u8(final_url)
            out = json.loads(res)
            return out['source'][0]['file']
        except:
            return json.dumps({"eror": "error occured while scrapping"})

    # def search(self, anime):
    #     page = requests.get(
    #         f'{BASE_URL}//search.html?keyword={anime}')
    #     soup = BeautifulSoup(page.content, 'html.parser')
    #     img, name, rel = soup.find_all('div', {'class': 'img'}), soup.find_all(
    #         'p', {'class': 'name'}), soup.find_all('p', {'class': 'released'})
    #     searchjson = []
    #     for i in range(len(img)):
    #         searchjson.append({"anime": name[i].getText(), "link": img[i].a['href'], "thumbnail": img[i].a.img['src'],
    #                            "release": rel[i].getText().replace(' ', '').replace('\n', '')})

    #     return searchjson

    def search2(self,anime):
        page = requests.get(f'{BASE_URL}//search.html?keyword={anime}')
        soup = BeautifulSoup(page.content, 'html.parser')
        return list(map(
            lambda it: {"anime":it['alt'],"thumbnail":it['src']},
            soup.select("#wrapper_bg > section > section.content_left > div > div.last_episodes > ul > li > div > a > img")
        ))

    def getanimeinfo(self, animeurlname):
        filteruri = animeurlname.replace(' ', '')
        page = requests.get(
            f'{BASE_URL}//category/{filteruri}')
        animeinfosoup = BeautifulSoup(page.content, 'html.parser')
        animeinfo = []
        reps = []
        # n = animeinfosoup.find('div', {'class': 'anime_info_episodes'}).h2.text
        for ep in animeinfosoup.find_all('a', {'href': '#'}):
            reps.append(ep.text)
        epcountreps = 0
        try:
            ind = reps[-1].index("-")
            epcountreps = reps[-1][ind+1:].replace(" ", "")
        except:
            epcountreps = reps[-1]
        for i in animeinfosoup.find_all('p', {'class': 'type'}):
            animeinfo.append(i.text.replace("\n", ""))
        tjson = []
        tjson.append({"type": animeinfo[0][5:], "plot": animeinfo[1][13:], "genre": animeinfo[2][6:].replace(
            '  ', ''), "released": animeinfo[3], "episodes_released": int(epcountreps)})
        return tjson

    def getifr(self, animeep, anime):
        page = requests.get(
            f"{BASE_URL}/{anime}-episode-{animeep}")
        epsoup = BeautifulSoup(page.content, 'html.parser')
        link = epsoup.find_all('li', {'class': 'streamsb'})[0].a['data-video']
        return link

    # def homepage(self):
    #     page = requests.get(
    #         f'{BASE_URL}')
    #     soup = BeautifulSoup(page.content, 'html.parser')
    #     img, name, rel = soup.find_all('div', {'class': 'img'}), soup.find_all(
    #         'p', {'class': 'name'}), soup.find_all('p', {'class': 'episode'})
    #     searchjson = []
    #     for i in range(len(img)):
    #         searchjson.append({"anime": name[i].getText(), "cover": img[i].a.img['src'],
    #                            "latestep": rel[i].getText().replace(' ', '').replace('\n', '')})

    #     return searchjson

    def homepage2(self):
        page = request('GET',BASE_URL).content
        soup = BeautifulSoup(page,'html.parser')
        return list(map(
            lambda it:  {"anime":it['alt'],"cover":it['src']},
            soup.select("#load_recent_release > div.last_episodes.loaddub > ul > li > div > a > img")
        ))

    def animeInfo2(self,anime):
        page = request('GET',BASE_URL+"category/"+anime).content
        soup = BeautifulSoup(page, 'html.parser')
        print(soup.select("#episode_related > li:nth-child(1) > a > div.name"))
        return list(map(
            lambda it:  {"type":it.select("p:nth-child(4) > a")[0]['title'],
                        "plot":it.select("p:nth-child(5)")[0].get_text(),
                        "genre":it.select("p:nth-child(6)")[0].get_text(),
                        "released":it.select("p:nth-child(6)")[0].get_text(),
                        "episodes_released":int(soup.select('#episode_page > li > a.active')[0]['ep_end'])},
            soup.select("#wrapper_bg > section > section.content_left > div.main_body > div:nth-child(2) > div.anime_info_body_bg")
        ))



# class GogoParser(GogoCrypto):
#     def __init__(self) -> None:
#         super().__init__(KEY,IV)
#         self.baseUrl,self.baseAjaxUrl,self.iframeReqHeaders,self.m3u8ReqHeaders = BASE_URL,AJAX_URL,GOGO_IFRAME_HEADERS,GOGO_M3U8_HEADERS
        
#     def getIframeUrl(self,url):
#         data = request("GET", url).text
#         surl = re.findall(r'goload.* s', data) 
#         return surl[0][:-3]
    
#     def getMsgFromIframe(self,url):
#         response = request("GET", url, headers=self.iframeReqHeaders, data={})
#         data = response.text
#         msg = re.findall(r'data-value.*><',data)[0]
#         msg = msg[11:-2]
#         return msg

#     def makeM3u8ReqUrl(self,msg):
#         print(msg)
#         new_url = self._decrypt(msg)
#         print(new_url)
#         print(type(new_url))
#         id_msg = new_url[:8].decode("utf-8")
#         new_id = self._encrypt(id_msg)
#         return self.baseAjaxUrl+"?id="+new_id+new_url[8:].decode("utf-8")+"&alias="+id_msg

#     def getM3u8(self,url):
#         response = request("GET", url, headers=self.m3u8ReqHeaders, data={})
#         data = json.loads(response.text)['data']
#         return self._decryptGogom3u8(data,KEY2).decode("utf-8")




# class VidStreamingParser(KdramaCrypto,GogoCrypto):
#     def __init__(self,baseUrl,baseAjaxUrl,iframeReqHeaders,m3u8ReqHeaders) -> None:
#         KdramaCrypto.__init__(self,KDRAMA_KEY,KDRAMA_IV)
#         super().__init__(KEY,IV)
#         self.baseUrl,self.baseAjaxUrl,self.iframeReqHeaders,self.m3u8ReqHeaders = baseUrl,baseAjaxUrl,iframeReqHeaders,m3u8ReqHeaders
    
#     def getMsgFromIframe(self,url):
#         response = request("GET", url, headers=self.iframeReqHeaders, data={})
#         data = response.text
#         msg = re.findall(r'data-value.*><',data)[0]
#         msg = msg[11:-2]
#         return msg

#     def makeM3u8ReqUrl(self,msg):
#         print(msg)
#         new_url = self._decrypt(msg)
#         print(new_url)
#         print(type(new_url))
#         id_msg = new_url[:8].decode("utf-8")
#         new_id = self._encrypt(id_msg)
#         return self.baseAjaxUrl+"?id="+new_id+new_url[8:].decode("utf-8")+"&alias="+id_msg