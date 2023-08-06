from youtube_transcript_api import YouTubeTranscriptApi
from clarku_youtube_crawler.CrawlerObject import _CrawlerObject
import pandas as pd
from configparser import ConfigParser
import json
import os
import asyncio

CONFIG = "config.ini"
config = ConfigParser(allow_no_value=True)
config.read(CONFIG)


class SubtitleCrawler(_CrawlerObject):
    def __init__(self):
        super().__init__()

    def _crawl(self, vid):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(vid)
            return transcript
        except:
            return None

    def crawl_csv(self, **kwargs):
        filename = kwargs.get("videos_to_collect", f"{self.CURRENT_ROOT}videos_to_collect.csv")
        video_id = kwargs.get("video_id", "videoId")
        save_dir = kwargs.get("sub_title_dir", f"{self.CURRENT_ROOT}{self.subtitle_subtitle_dir}")
        core = kwargs.get("core", 8)
        accepted_ext = [".csv", ".xlsx"]

        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        ext = ".csv"
        if filename:
            file, ext = os.path.splitext(filename)
            if ext not in accepted_ext:
                raise ValueError(f"{ext} is not an accepted file type")

        if filename is None:
            raise ValueError("Can't find video list to crawl. Specify the video CSV by filename=YOUR_PATH")

        if ext == ".csv":
            df = pd.read_csv(filename)
        else:
            df = pd.read_excel(filename)

        asyncio.run(self.start_crawling(df, video_id, save_dir, core))

    async def start_crawling(self, df, video_id, save_dir, core):
        counter = 0
        for vid in df[video_id]:
            if not os.path.exists(save_dir + vid[1:] + ".json"):
                print(f"crawling subtitle: {vid[1:]}")
                if counter % core == 0 or counter == len(df) - 1:
                    await asyncio.gather(self.get_subscription(vid, save_dir))
                else:
                    asyncio.gather(self.get_subscription(vid, save_dir))
            else:
                print(f'Subtitle {vid} crawled skipped')
            counter += 1

    async def get_subscription(self, vid, save_dir):
        transcript = self._crawl(vid[1:])
        if transcript:
            with open(save_dir + vid[1:] + ".json", 'w+') as fp:
                fp.write(json.dumps(transcript) + "\n")
            print(f'Subtitle {vid} crawled')
        else:
            print(f'Subtitle {vid} crawled failed')
