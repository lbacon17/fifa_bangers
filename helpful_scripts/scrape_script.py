from bs4 import BeautifulSoup
import urllib.request as urllib2
from urllib.request import urlopen, Request
import re

html_page = "https://www.sportingnews.com/ca/soccer/list/fifa-20-every-fifa-video-game-cover-since-inception/jlyrte09xmvb1xxg2x1gxhj3w"
hdr = {"User-Agent": "Mozilla/5.0"}
req = Request(html_page, headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page)
images = []
for img in soup.findAll("img"):
    images.append(img.get("src"))

print(images)
