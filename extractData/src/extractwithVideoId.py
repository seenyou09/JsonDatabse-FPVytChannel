# Created python module to find channels related to a specific video ID. It extracts statistics for these channels, focusing on subscribers, views, total videos, categories, and keywords.


import pandas as pd
from bs4 import BeautifulSoup
import requests
from googleapiclient.discovery import build
import json
from _youtubeAPI.ytChannelStat import yt_channel_stats


api_key = "AIzaSyAj5k5KzAy-rgnnZS-iVU-nLNsZ2Bltnos"
video_id = "YJsnMCcjSbA"
youtube = build("youtube", "v3", developerKey=api_key)

class yt_search_relatedChannel_withVideoId:
    
    def __init__(self, video_id, api_key):
        self.video_id = video_id
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        self.stats_list = self.get_related_withVideoId()
        self.channel_id = self.get_onlyChannelId()

        
    def get_related_withVideoId(self):
        self.stats_list = []
        request = self.youtube.search().list(
            maxResults = 10000, 
            part="snippet",
            order="videoCount",
            relatedToVideoId = self.video_id,
            type="video"
        )         
        response = request.execute()
        for video in response["items"]:
            cid = video["snippet"]["channelId"]
            ct = video["snippet"]["channelTitle"]
            self.statDict = dict(channelId = cid, channelTitle = ct)
            self.stats_list.append(self.statDict)
    
        return self.stats_list
    def get_onlyChannelId(self):
        self.channel_id = []
        for items in self.stats_list:
            self.channel_id.append(items["channelId"])
        
        return self.channel_id
    
    def get_relatedchannel_withChannelId(self):
        f_list = {}
        for id in self.channel_id:
            url = "https://www.youtube.com/channel/" + id
            #find the stats for all related channel
            item = yt_channel_stats(url, api_key, youtube)
            info = item.clean_dataforCSV()
            key = info["Channel_id"]
            if key in f_list.keys():
                pass
            else:
                f_list[key] = info

        f_list
        
        df = pd.DataFrame.from_dict(f_list, orient='index')
        return df 



if __name__ == "__main__":

    video_id = "13OtZFWdhwQ"
    trial =yt_search_relatedChannel_withVideoId(video_id, api_key)
    f_df = trial.get_relatedchannel_withChannelId()
    excel_name = "related_channel" + str(video_id) + ".xlsx"
    f_df.to_excel(excel_name, index=False)



'''
    Export to csv
    excel_file_path = 'final.csv'
    df.to_csv(excel_file_path)
    
'''
    
