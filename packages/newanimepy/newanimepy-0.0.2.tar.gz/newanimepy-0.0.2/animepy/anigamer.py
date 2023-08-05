#This program is made by Misaka0502

from .response import anigamer, anisearch

class Anigamer:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def homepage(self):
        return anigamer.AniResponse()

    def anisearch(self, keywords: str):
        return anisearch.AniSearchResponse(keywords)
