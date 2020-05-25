import requests
import shutil
from datetime import datetime
import random

key = []

user_agent_list = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


class Scrapper:
    def __init__(self, username, id=None):
        self.username = username
        self.key = random.choice(key)
        if (id):
            self.id = id
        else:
            self.id = self.get_id_from_username()
        self.videoCount = 0
        self.viewCount = 0
        self.subscriberCount = 0
        self.averageView = 0.0
        self.playlists = []
        self.count = 1

    def get_id_from_username(self):
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}
        self.key = random.choice(key)

        id = requests.get(
            f"https://www.googleapis.com/youtube/v3/channels?key={self.key}&forUsername={self.username}&part=id",
            headers=headers).json()[
            'items'][0]['id']
        return id

    def get_stats(self):
        self.key = random.choice(key)

        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.id}&key={self.key}"
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}

        stat = requests.get(url, headers=headers).json()[
            'items'][0]['statistics']
        self.viewCount = int(stat['viewCount'])
        self.subscriberCount = int(stat['subscriberCount'])
        self.videoCount = int(stat['videoCount'])
        self.averageView = self.viewCount / self.videoCount
        print(f"[+] Info : finished getting stats")

    def get_videos(self):

        for playlist in self.playlists:
            user_agent = random.choice(user_agent_list)
            headers = {'User-Agent': user_agent}
            self.key = random.choice(key)
            video_info = requests.get(
                f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=1000&playlistId={playlist}&key={self.key}",
                headers=headers).json()

            items = video_info['items']

            for item in items:
                try:
                    thumbnail = item['snippet']['thumbnails']['medium']['url']
                    video_id = thumbnail.split("vi/")[1].split("/")[0]
                    views = int(self.get_views_from_id(video_id))
                    score = 0.5 * (views / self.averageView) + \
                        0.5 * (views / self.subscriberCount)
                    if score < 1:
                        category = "not"
                    elif score <= 2:
                        category = "well"
                    else:
                        category = "viral"
                    image = requests.get(thumbnail, stream=True)
                    with open(f"{category}/{datetime.now().microsecond}.jpg", "wb") as img:
                        shutil.copyfileobj(image.raw, img)
                    print(
                        f"{self.count} / {self.videoCount}    ========    completed {(self.count / self.videoCount) * 100}%")
                    self.count = self.count + 1
                    if self.count == 10000:
                        exit()
                except:
                    pass

    def get_views_from_id(self, video_id):
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}
        self.key = random.choice(key)

        video_stat = requests.get(
            f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails,statistics&id={video_id}&key={self.key}",
            headers=headers).json()
        return video_stat['items'][0]['statistics']['viewCount']

    def get_playlist(self, token=None):
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}
        self.key = random.choice(key)

        if token is None:

            playlist_info = requests.get(
                f"https://www.googleapis.com/youtube/v3/playlists?part=contentDetails&channelId={self.id}&key={self.key}",
                headers=headers).json()
        else:
            playlist_info = requests.get(
                f"https://www.googleapis.com/youtube/v3/playlists?part=contentDetails&channelId={self.id}&key={self.key}&pageToken={token}",
                headers=headers).json()
        if 'nextPageToken' in playlist_info:
            token = playlist_info['nextPageToken']
        else:
            token = None
        items = playlist_info['items']
        for i in range(len(items)):
            self.playlists.append(items[i]['id'])
            print(f"[+] Info : Adding {items[i]['id']} as playlist")

        if token is not None:
            self.get_playlist(token)
        else:
            print(f"[+] Info : playlist count is {len(self.playlists)}")


s = Scrapper("BuzzFeedVideo")
s.get_stats()
s.get_playlist()
s.get_videos()
