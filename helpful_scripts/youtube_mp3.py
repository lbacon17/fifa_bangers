from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from urllib import request
from lxml import etree
import os

url_strings = open("helpful_scripts/yt_urls.txt", "r").readlines()
yt_urls = []
for string in url_strings:
    if "/" not in string:
        print(f"Skipping {string}...")
        continue
    yt_urls.append(string)
destination = "media/audio"
for yt_url in yt_urls:
    try:
        video_title = etree.HTML(request.urlopen(yt_url).read().decode("utf-8"))
        filename = (
            video_title.xpath("//title")[0].text
            if len(video_title.xpath("//title")) > 0
            else "No Title"
        )
        filename = (
            filename.replace(" ", "_")
            .replace(":", "")
            .replace("(", "")
            .replace(")", "")
            .replace("'", "")
            .replace("’", "")
            .replace("/", "")
            .replace("!", "")
            .replace("?", "")
            .replace("[", "")
            .replace("]", "")
            .replace("|", "")
            .replace("'", "")
            .replace(",", "")
            .replace('"', "")
            .replace("&", "")
            .replace("+", "")
            .replace("é", "e")
            .replace("ê", "e")
            .replace("ë", "e")
            .replace("à", "a")
            .replace("ä", "a")
            .replace("ā", "a")
            .replace("ï", "i")
            .replace("ç", "c")
            .replace("ö", "o")
            .replace("ü", "u")
            .replace("ñ", "n")
        )
        if os.path.exists(f"{destination}/{filename}.mp4"):
            print(f"{filename}.mp4 exists.")
            continue
        YouTube(yt_url).streams.first().download(
            destination, filename=f"{filename}.mp4"
        )
        print(f"Downloaded {filename}.mp4!")
        yt = YouTube(yt_url)
        yt.streams.filter(only_audio=True, progressive=True)
    except VideoUnavailable as e:
        print("Video " + yt_url.split("v=")[-1] + " has been removed from YouTube.")
        continue
