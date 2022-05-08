from pytube import YouTube

yt_urls = ["https://www.youtube.com/watch?v=zY3Ni6RS6xk"]
destination = "media/audio"
for yt_url in yt_urls:
    YouTube(yt_url).streams.first().download(destination)
    yt = YouTube(yt_url)
    yt.streams.filter(only_audio=True, progressive=True)
