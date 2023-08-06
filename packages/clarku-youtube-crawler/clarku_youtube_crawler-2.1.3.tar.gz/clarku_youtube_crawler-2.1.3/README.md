# clarku-youtube-crawler

Clark University YouTube crawler and JSON decoder for YouTube json. Please read documentation in ``DOCS``

Pypi page: "https://pypi.org/project/clarku-youtube-crawler/"

## Installing
To install,

``pip install clarku-youtube-crawler``

The crawler needs multiple other packages to function. 
If missing requirements (I already include all dependencies so it shouldn't happen), download <a href="https://github.com/ClarkUniversity-NiuLab/clarku-youtube-crawler/blob/master/requirements.txt">``requirements.txt`` </a> .
Navigate to the folder where it contains requirements.txt and run 

``pip install -r requirements.txt``


## Upgrading
To upgrade

``pip install clarku-youtube-crawler --upgrade``

Go to the project folder, delete config.ini if it is already there.

## YouTube API Key
- Go to https://cloud.google.com/, click console, and create a project. Under Credentials, copy the API key.
- In your project folder, create a "DEVELOPER_KEY.txt" file (must be this file name) and paste your API key. 
- You can use multiple API keys by putting them on different lines in DEVELOPER_KEY.txt. 
- The crawler will use up all quotas of one key and try next one, until all quotas are used up.



## Example usage
Case 1: crawl videos by keywords, 
```
import clarku_youtube_crawler as cu

# Crawl all JSONs
crawler = cu.RawCrawler()
crawler.build("low visibility")
crawler.crawl("low visibility", start_date=14, start_month=12, start_year=2020, day_count=5)
crawler.crawl("blind", start_date=14, start_month=12, start_year=2020, day_count=5)
crawler.merge_to_workfile()
crawler.crawl_videos_in_list(comment_page_count=1)
crawler.merge_all(save_to='low visibility/all_videos.json')

# Convert JSON to CSV
decoder = cu.JSONDecoder()
decoder.json_to_csv(data_file='low visibility/all_videos.json')

# Crawl subtitles from CSV
# If you don't need subtitles, delete the following lines
subtitleCrawler = cu.SubtitleCrawler()
subtitleCrawler.build("low visibility")
subtitleCrawler.crawl_csv(
    videos_to_collect="low visibility/videos_to_collect.csv",
    video_id="videoId",
    sub_title_dir="low visibility/subtitles/"
)

```

Case 2: crawl a videos by a list of ids specified by videoId column in an input CSV
```
import clarku_youtube_crawler as cu

crawler = cu.RawCrawler()
work_dir = "blind"
crawler.build(work_dir)

# update videos_to_collect.csv to your csv file. Specify the column of video id by video_id
# video ids must be ":" + YouTube video id. E.g., ":wl4m1Rqmq-Y"

crawler.crawl_videos_in_list(video_list_workfile="videos_to_collect.csv",
                             comment_page_count=1,
                             search_key="blind",
                             video_id="videoId"
                             )
crawler.merge_all(save_to='all_raw_data.json')
decoder = cu.JSONDecoder()
decoder.json_to_csv(data_file='all_raw_data.json')

# Crawl subtitles from CSV
# If you don't need subtitles, delete the following lines
subtitleCrawler = cu.SubtitleCrawler()
subtitleCrawler.build(work_dir)
subtitleCrawler.crawl_csv(
    videos_to_collect="videos_to_collect.csv",
    video_id="videoId",
    sub_title_dir=f"YouTube_CSV/subtitles/"
)

```

Case 3: Search a list of channels by search keys, then crawl all videos belonging to those channels.
```
import clarku_youtube_crawler as cu

chCrawler = cu.ChannelCrawler()
work_dir = "low visibility"
chCrawler.build(work_dir)
# You can search different channels. All results will be merged
chCrawler.search_channel("low visibility")
chCrawler.search_channel("blind")
chCrawler.merge_to_workfile()
chCrawler.crawl()

# Crawl videos posted by selected channels. channels_to_collect.csv file has which search keys find each channel
crawler = cu.RawCrawler()
crawler.build(work_dir)
crawler.merge_to_workfile(file_dir=work_dir + "/video_search_list/")
crawler.crawl_videos_in_list(comment_page_count=1)
crawler.merge_all()

# Convert JSON to CSV
decoder = cu.JSONDecoder()
decoder.json_to_csv(data_file=work_dir + '/all_videos_visibility.json')

# Crawl subtitles from CSV
# If you don't need subtitles, delete the following lines
subtitleCrawler = cu.SubtitleCrawler()
subtitleCrawler.build(work_dir)
subtitleCrawler.crawl_csv(
    videos_to_collect=work_dir+"/videos_to_collect.csv",
    video_id="videoId",
    sub_title_dir=work_dir+"/subtitles/"
)
```

Case 4: You already have a list of channels. You want to crawl all videos of the channels in the list:
```
import clarku_youtube_crawler as cu

work_dir = 'disability'
chCrawler = cu.ChannelCrawler()
chCrawler.build(work_dir)

chCrawler.crawl(filename='mturk_test.csv', channel_header="Input.channelId")

# Crawl videos posted by selected channels
crawler = cu.RawCrawler()
crawler.build(work_dir)
crawler.merge_to_workfile(file_dir=work_dir + "/video_search_list/")
crawler.crawl_videos_in_list(comment_page_count=10)  # 100 comments per page, 10 page will crawl 1000 comments

crawler.merge_all()
#
# Convert JSON to CSV
decoder = cu.JSONDecoder()
decoder.json_to_csv(data_file=work_dir + '/all_videos.json')

# Crawl subtitles from CSV
subtitleCrawler = cu.SubtitleCrawler()
subtitleCrawler.build(work_dir)
subtitleCrawler.crawl_csv(
    videos_to_collect=work_dir + "/videos_to_collect.csv",
    video_id="videoId",
    sub_title_dir=work_dir + "/subtitles/"
)
```


