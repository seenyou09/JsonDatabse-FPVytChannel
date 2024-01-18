# 1. The script initializes with the provided YouTube channel URL, API key, and YouTube API instance.
# 2. It fetches the YouTube channel ID from the URL.
# 3. Channel name and upload ID are obtained using the YouTube API.
# 4. A list of video IDs associated with the channel is fetched.
# 5. Detailed statistics for each video in the video list are obtained.
# 6.The resulting data is converted into a pandas DataFrame.

import pandas as pd
from bs4 import BeautifulSoup
import requests
from googleapiclient.discovery import build
import json

api_key = "AIzaSyAj5k5KzAy-rgnnZS-iVU-nLNsZ2Bltnos"

youtube = build("youtube", "v3", developerKey=api_key)

class yt_video_stats:
    def __init__(self, url, api_key, youtube):
        self.url = url
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        self.id = self.get_id()
        self.channel_name, self.upload_id = self.get_upload_id()
        self.video_list = self.get_video_list()
        
    def get_id(self):
        # Send a GET request to the webpage containing the link element
        response = requests.get(self.url)
    
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
    
        rss_link = soup.find('link', {'rel': 'alternate', 'type': 'application/rss+xml'})
    
        if rss_link:
            rss_url = rss_link.get('href')
            rss_url = rss_url.split("channel_id=",1)[1]
            return rss_url
        else:
            return None
    
    def get_upload_id(self):
        request = youtube.channels().list(
            part="snippet,contentDetails",
            id=self.id
        )
        response = request.execute()
        self.channel_name=response['items'][0]['snippet']['title']
        self.upload_id = response["items"][0]['contentDetails']['relatedPlaylists']['uploads']
        return self.channel_name, self.upload_id
    
    def get_video_list(self):
        video_list = []
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=self.upload_id,
            maxResults=50
        )
        next_page = True
        while next_page:
            response = request.execute()
            data = response['items']
    
            for video in data:
                video_id = video['contentDetails']['videoId']
                if video_id not in video_list:
                    video_list.append(video_id)
    
            # Do we have more pages?
            if 'nextPageToken' in response.keys():
                next_page = True
                request = youtube.playlistItems().list(
                    part="snippet,contentDetails",
                    playlistId=self.upload_id,
                    pageToken=response['nextPageToken'],
                    maxResults=50
                )
            else:
                next_page = False
    
        return video_list
    def get_video_details(self):
        stats_list=[]
    
        # Can only get 50 videos at a time.
        for i in range(0, len(self.video_list), 50):
            request= youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=self.video_list[i:i+50]
            )
    
            data = request.execute()
            for video in data['items']:
                title=video['snippet']['title']
                published=video['snippet']['publishedAt']
                description=video['snippet']['description']
                try:
                    tag_count= len(video['snippet']['tags'])
                except:
                    tag_count= " "
                view_count=video['statistics'].get('viewCount',0)
                like_count=video['statistics'].get('likeCount',0)
                try:
                    dislike_count=video['statistics'].get('dislikeCount',0)
                except:
                    dislike_count= " "
                try:    
                    comment_count=video['statistics'].get('commentCount',0)
                except:
                    comment_count= " "
                stats_dict=dict(name=self.channel_name, title=title, description=description, published=published, tag_count=tag_count, view_count=view_count, like_count=like_count, dislike_count=dislike_count, comment_count=comment_count)
                stats_list.append(stats_dict)
    
        return stats_list
    def updateJson(self,filename):
        entry = []
        entry = self.get_video_details()

        with open(filename, "r") as file:
            data = json.load(file)
            
        
        data.append(entry)
        

        
        with open(filename,"w") as file:
            json.dump(data, file)
        
            
    
if __name__ == "__main__":
    filename = "video_stats_df"
    trial = yt_video_stats("https://www.youtube.com/@TechWithTim", api_key, youtube)
    trial_dict = trial.get_video_details()
    videoDescription_df = pd.DataFrame(trial_dict)
    videoDescription_df