key= "" #your API key here

import urllib.request
import json

YouTubers = [
    {
        "user": "Buzzfeed",
        "id": "UCpko_-a4wgz2u_DgDgd9fqA",
        "uploads_id": "UUpko_-a4wgz2u_DgDgd9fqA"
    },
    #add more youtubers here.
]


class Scraper:
    def __init__(self, uid, upid, user):
        self.id = uid
        self.upid = upid
        self.user = user

    def add_stats(self):
        r = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + self.id + "&key=" + key)
        rstring = r.read().decode('utf-8')
        stats = json.loads(rstring)['items'][0]['statistics']
        self.subs = int(stats['subscriberCount'])
        self.total_views = int(stats['viewCount'])
        self.video_count = int(stats['videoCount'])
        self.average_views = self.total_views/self.video_count

    def calculate_view_score(self, view):
        return 0.5*(view/self.average_views) + 0.5*(view/self.subs)

    def get_video_list(self, token="None", start=0):
        if token=="None":
            req = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&playlistId="+ self.upid +"&key=" + key)
        else:
            req = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&playlistId="+ self.upid +"&key=" + key +"&pageToken=" + token)
        string = req.read().decode('utf-8')
        json_obj = json.loads(string)
        if 'nextPageToken' in json_obj:
            token = json_obj['nextPageToken']
        else:
            token = "None"
        for i in range(50):
            try:
                views = self.views_from_id(json_obj['items'][i]['snippet']['resourceId']['videoId'])
                thumb_link = json_obj['items'][i]['snippet']['thumbnails']['default']['url']
                score = self.calculate_view_score(int(views))
                print(i+start, score, thumb_link)
                if score<1:
                    category = "not_viral"
                elif score<=2:
                    category = "does_well"
                else:
                    category = "viral"
                urllib.request.urlretrieve(thumb_link, "{}/{}{}.jpg".format(category, self.user, i+start))
            except:
                pass
        print("token is "+ token)
        if token != "None":
            return self.get_video_list(token, start+50)

    
    def views_from_id(self, video_id):
        req = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/videos?part=contentDetails,statistics&id=" + video_id + "&key="+ key)
        string = req.read().decode('utf-8')
        json_obj = json.loads(string)
        return json_obj['items'][0]['statistics']['viewCount']

for tuber in YouTubers:
    scraper = Scraper(tuber["id"], tuber["uploads_id"], tuber["user"])
    scraper.add_stats()
    scraper.get_video_list()
