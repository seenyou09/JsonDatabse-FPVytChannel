
# The provided Python code defines a class called yt_channel_stats, 
# which is designed to extract and process statistics and information
# about a YouTube channel. The class takes a YouTube channel URL, an API key, 
# and a YouTube API object as input parameters. 

import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import pandas as pd


api_key = "AIzaSyDqYcV4mJWQImAteWnLeIzVgO4X9fO-mIY"
youtube = build("youtube", "v3", developerKey=api_key)


class yt_channel_stats:
    def __init__(self, url, api_key, youtube):
        self.url = url
        self.id = self.get_id()

        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        self.data = self.get_info()
        self.clean_data = self.clean_dataforCSV()

    def get_id(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        rss_link = soup.find('link', {'rel': 'alternate', 'type': 'application/rss+xml'})
        if rss_link:
            rss_url = rss_link.get('href')
            rss_url = rss_url.split("channel_id=", 1)[1]
            return rss_url
        else:
            return ""
        

    def get_info(self):
        request = self.youtube.channels().list(
            part="snippet,statistics,brandingSettings,topicDetails",
            id=self.id
        )
        response = request.execute()

        cn = response['items'][0]['snippet']['title']
        s = response['items'][0]['statistics']['subscriberCount']
        v = response['items'][0]['statistics']['viewCount']
        tv = response['items'][0]['statistics']['videoCount']
        
        cg = []
        try:
            cg = response['items'][0]['topicDetails']['topicCategories']
            f_cg = [url.split("wiki/")[1] for url in cg]
                
        except:
            cg = []
            f_cg = []
        
        f_k=''
        try:
            k = response['items'][0]['brandingSettings']['channel']['keywords']
            f_k = k.split()
        except:
            k = ""
            f_k =""
        self.data = dict(Channel_name=cn, Channel_id=self.id, Video_Statistic={}, Channel_Statistic={
            "Subscribers": int(s),
            "Views": int(v),
            "Total_videos": int(tv),
            "Categories": f_cg,
            "Keywords": f_k
        })

        return self.data
    
    def clean_dataforCSV(self):
        items = self.data["Channel_Statistic"]
        subscribers = items["Subscribers"]
        views = items["Views"]
        total_videos = items["Total_videos"]
        categories = items["Categories"]
        keywords = items["Keywords"]
        self.clean_data = {
            "Channel_name": self.data["Channel_name"],
            "Channel_id" : self.data["Channel_id"],
            "Subscribers": subscribers,
            "Views": views,
            "Total_videos": total_videos,
            "Categories": categories,
            "Keywords": keywords
        }
        return self.clean_data
