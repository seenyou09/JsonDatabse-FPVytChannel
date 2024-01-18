
# This Python script uses the module ytChannelStat and yt_search_relatedChannel_withVideoId to only extract channel_id

import pandas as pd
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from _youtubeAPI.ytChannelStat import yt_channel_stats
from extractwithVideoId import yt_search_relatedChannel_withVideoId


api_key = "AIzaSyAj5k5KzAy-rgnnZS-iVU-nLNsZ2Bltnos"
video_id = "YJsnMCcjSbA"
youtube = build("youtube", "v3", developerKey=api_key)

joshua =yt_search_relatedChannel_withVideoId(video_id, api_key)

id_list = joshua.get_onlyChannelId()

f_list = {}
for id in id_list:
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


if __name__ == "__main__":

    df = pd.DataFrame.from_dict(f_list, orient='index')
    excel_name = "related_channel" + str(video_id) + ".xlsx"
    df.to_excel(excel_name, index=False)



'''
    Export to csv
    excel_file_path = 'final.csv'
    df.to_csv(excel_file_path)
    
'''