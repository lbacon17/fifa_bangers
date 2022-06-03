from pytube import YouTube
from urllib import request
from lxml import etree

url_strings = open("helpful_scripts/yt_urls.txt", "r").readlines()
yt_urls = []
for string in url_strings:
    yt_urls.append(string)
destination = "media/audio"
for yt_url in yt_urls:
    video_title = etree.HTML(request.urlopen(yt_url).read().decode("utf-8"))
    filename = (
        video_title.xpath("//title")[0].text
        if len(video_title.xpath("//title")) > 0
        else "No Title"
    )
    filename = filename.replace(" ", "_")
    YouTube(yt_url).streams.first().download(destination, filename=f"{filename}.mp4")
    yt = YouTube(yt_url)
    yt.streams.filter(only_audio=True, progressive=True)
