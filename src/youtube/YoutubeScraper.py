from lxml.html import fromstring
from pytube import YouTube 
import yt_dlp


class YoutubeScraper:

    def __init__(self, response_text, url):
        self.parser = fromstring(response_text)
        self.url = url


    def download_audio(self, output_path="./output"):
        ydl_opts = {
            "format": "bestaudio[ext=m4a]/bestaudio",
            "outtmpl": f"{output_path}/%(title)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "ffmpeg-location": "/usr/bin/ffmpeg",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
                

    def extract_yotube_video(self):

        title = self.parser.xpath("//title//text()")
        title = ' '.join(title).strip()
        title = title.split(" - YouTube")[0]

        channel = self.parser.xpath("//link[contains(@itemprop, 'name')]//@content")
        channel = ' '.join(channel).strip()

        self.download_audio()

        return {
            "title": title,
            "channel": channel,
            "media_url": self.url,
        }

    def extract_data(self):
        if "www.youtube.com/shorts/" in self.url:
            return None
        elif "www.youtube.com/watch" in self.url:

            return self.extract_yotube_video()
        
