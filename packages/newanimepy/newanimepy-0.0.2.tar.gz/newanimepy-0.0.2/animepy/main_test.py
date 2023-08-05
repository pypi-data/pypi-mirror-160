from .anigamer import Anigamer
from .response import anigamer
import re

animes = Anigamer()
#print(animes.homepage())
#print(animes.homepage().ani['name'][1])
#print(animes.homepage().ani['watch'][1])
#print(anigamer.AnigamerList().homepageinfo())
#aaa = input("Please input:")
#print(animes.anisearch(aaa).sani)
with open('animepy/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

print(version)