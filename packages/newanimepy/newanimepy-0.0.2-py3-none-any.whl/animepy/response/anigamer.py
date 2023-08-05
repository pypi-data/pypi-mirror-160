from typing import Dict, List

from bs4 import BeautifulSoup
import requests

from .errors import Error_type

class AnigamerList:
    #Crawler code from https://blog.jiatool.com/posts/gamer_ani_spider
    def __init__(self):
        c_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
        data = requests.get("https://ani.gamer.com.tw/", headers=c_headers)
        self.namelist = []
        self.watchlist = []
        self.episodelist = []
        self.hreflist = []
        self.pictlist = []
        if data.status_code == 200:
            soup = BeautifulSoup(data.text, 'html.parser')
            all_anime = soup.select_one('.timeline-ver > .newanime-block')
            new_animes = all_anime.select('.newanime-date-area:not(.premium-block)')
            for new_anime in new_animes:
                self.all = new_anime
                self.name: str = new_anime.select_one('.anime-name > p').text.strip()
                self.namelist.append(self.name)
                self.watch: str = new_anime.select_one('.anime-watch-number > p').text.strip()
                self.watchlist.append(self.watch)
                self.episode: str = new_anime.select_one('.anime-episode').text.strip()
                self.episodelist.append(self.episode)
                self.href: str = 'https://ani.gamer.com.tw/' + new_anime.select_one('a.anime-card-block').get('href')
                self.hreflist.append(self.href)
                self.pict: str = new_anime.select_one('.anime-blocker > img').get('src')
                self.pictlist.append(self.pict)
        else:
            Error_type().status_error(data.status_code)

    def homepageinfo(self) -> Dict:
        ani_info = {
            "name": "",
            "watch": "",
            "episode": "",
            "href": "",
            "pict": ""
        }
        if ani_info["name"] == "":
            ani_info["name"] = self.namelist
        if ani_info["watch"] == "":
            ani_info["watch"] = self.watchlist
        if ani_info["episode"] == "":
            ani_info["episode"] = self.episodelist
        if ani_info["href"] == "":
            ani_info["href"] = self.hreflist
        if ani_info["pict"] == "":
            ani_info["pict"] = self.pictlist
        
        return ani_info

class AniResponse:
    def __init__(self):
        self.ani = AnigamerList().homepageinfo()
        #self.ani: List[AnigamerList] = [AnigamerList().homepageinfo()]
