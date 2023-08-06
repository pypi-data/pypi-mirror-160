from select import select
from requests import request
from bs4 import BeautifulSoup
import re,json


class Manhwa18Parser:
    def __init__(self):
        self.HOST_URL = 'https://manhwa18.cc/'
        self.SEARCH_URL = self.HOST_URL+'search?q='

    def search(self,key):
        res = request('GET',self.SEARCH_URL+key).content
        soup = BeautifulSoup(res,'html.parser')
        return list(map(
            lambda it: {"cover":it['src'],"name":it['alt']},
            soup.select('body > div.manga-content.wleft > div > div > div > div.manga-lists > div > div > div.thumb > a > img')
        ))

    def loadChapters(self,query):
        page = request('GET',self.HOST_URL+'webtoon/'+query).content
        soup = BeautifulSoup(page,'html.parser')
        return list(map(
            lambda it:  {"chapterLink":it['href'],"chapter":it.get_text()},
            soup.select("#chapterlist > ul > li > a")
        ))

    def loadImages(self,chLink):
        page = request('GET',chLink).content
        soup = BeautifulSoup(page,'html.parser')
        return list(map(
            lambda it:  it['src'],
            soup.select("div.read-content.wleft.tcenter > img")
        ))

    def proxyImages(self,imgLink):
        headers = { "referer":"https://manhwa18.cc/",
                    "authority":"img01.iwa-18cc.xyz",
                    "user-agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
                }
        return request('GET',imgLink,headers=headers).content



m = Manhwa18Parser()
print(m.search("secr"))