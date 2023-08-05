from typing import Dict, List

from bs4 import BeautifulSoup
import requests

from .errors import Error_type

class SAnigamer:
    def __init__(self, keyword: str):
        c_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
        data = requests.get('https://ani.gamer.com.tw/search.php?kw={}'.format(keyword), headers=c_headers)
        self.namelist = []
        self.watchlist = []
        self.episodelist = []
        self.yearlist = []
        self.hreflist = []
        self.pictlist = []
        if data.status_code == 200:
            soup = BeautifulSoup(data.text, 'html.parser')
            all_anime = soup.select_one('.animate-theme-list > .theme-list-block')
            animes = all_anime.select('.theme-list-main')
            for anime_result in animes:
                self.all = anime_result
                self.name: str = anime_result.select_one('.theme-info-block > p').text.strip()
                self.namelist.append(self.name)
                self.watch: str = anime_result.select_one('.show-view-number > p').text.strip()
                self.watchlist.append(self.watch)
                self.episode: str = anime_result.select_one('.theme-number').text.strip()
                self.episodelist.append(self.episode)
                self.year: str = anime_result.select_one('.theme-time').text.strip()
                self.yearlist.append(self.year[3:])
                self.href: str = 'https://ani.gamer.com.tw/' + anime_result.get('href')
                self.hreflist.append(self.href)
                self.pict: str = anime_result.select_one('.theme-img-block > img').get('src')
                self.pictlist.append(self.pict)
            if self.namelist == [] and self.watchlist == [] and self.episodelist == [] and self.yearlist == [] and self.hreflist == [] and self.pictlist == []:
                print(Error_type().no_result())
        else:
            print(Error_type().status_error(data.status_code))

    def Searchinfo(self) -> Dict:
        ani_search = {
            "name": "",
            "watch": "",
            "episode": "",
            "date": "",
            "href": "",
            "pict": ""
        }
        if ani_search["name"] == "":
            ani_search["name"] = self.namelist
        if ani_search["watch"] == "":
            ani_search["watch"] = self.watchlist
        if ani_search["episode"] == "":
            ani_search["episode"] = self.episodelist
        if ani_search["date"] == "":
            ani_search["date"] = self.yearlist
        if ani_search["href"] == "":
            ani_search["href"] = self.hreflist
        if ani_search["pict"] == "":
            ani_search["pict"] = self.pictlist
        
        return ani_search

class AniSearchResponse:
    def __init__(self, keywords: str):
        if keywords == "":
            print(Error_type().no_keyword())
        else:
            self.sani = SAnigamer(keyword=keywords).Searchinfo()