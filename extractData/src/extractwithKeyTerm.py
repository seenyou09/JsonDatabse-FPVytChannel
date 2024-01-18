# This Python script utilizes the YouTube Data API to search for YouTube channels related to a specified search term (in this case, "drone"). The script then retrieves relevant statistics for these channels, focusing on the channel's subscribers, views, total videos, categories, and keywords. The collected data is organized into a Pandas DataFrame and exported to an Excel file for further analysis.

from googleapiclient.discovery import build
from _youtubeAPI.ytChannelStat import yt_channel_stats
import pandas as pd


api_key = "AIzaSyAj5k5KzAy-rgnnZS-iVU-nLNsZ2Bltnos"
youtube = build("youtube", "v3", developerKey=api_key)




class yt_search_keyTerm:
    def __init__(self, term, api_key, youtube):
        self.term = term
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        self.stats_list = []
        self.stats_list = self.get_new_videos()
        self.channel_id = self.get_onlyChannelId()
    
    def get_new_videos(self):
        request = youtube.search().list(
            maxResults = 100, 
            part="snippet",
            order="videoCount",
            publishedAfter="2022-01-01T17:36:11Z",
            q=self.term,
    
            type="channel"
        )
        response = request.execute()
        for video in response["items"]:
            cid = video["snippet"]["channelId"]
            ct = video["snippet"]["channelTitle"]
            statDict = dict(channelId = cid, channelTitle = ct)
            self.stats_list.append(statDict)
        return self.stats_list
    
    def get_onlyChannelId(self):
        self.channel_id = []
        for items in self.stats_list:
            self.channel_id.append(items["channelId"])
        
        return self.channel_id
    def get_relatedchannel_withKeyterm(self):

        f_list = []
        for id in self.channel_id:
            url = "https://www.youtube.com/channel/" + id
            #find the stats for all related channel
            item = yt_channel_stats(url, api_key, youtube)
            info = item.clean_dataforCSV()
            if info["Subscribers"] in f_list:
                pass
            else:
                f_list.append(info)
        
        df = pd.DataFrame(f_list)
        
        return df
        



if __name__ == "__main__":
    term = "drone"
    trial = yt_search_keyTerm(term, api_key, youtube)
    f_df = trial.get_relatedchannel_withKeyterm()

    # Export the DataFrame to Excel
    excel_name = "related_channel-" + str(term) + ".xlsx"
    f_df.to_excel(excel_name, index=False)



        
        