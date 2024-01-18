from extractData.src.extractwithVideoId import yt_search_relatedChannel_withVideoId
from _youtubeAPI.videoStatsdicTojson import yt_channel_vid_statistic
from googleapiclient.discovery import build
import pandas as pd



#Read the list and convert to dictionary 
df = pd.read_excel('/Users/seanyoo/Desktop/buildingJsonDatabse-FPVpilotsYT/filterData/json-input/new1.0-20.xlsx')
video_ids = {}
video_ids = dict(zip(df['Video_id'], df['Types']))

api_key = "AIzaSyDqYcV4mJWQImAteWnLeIzVgO4X9fO-mIY"
#api_key = "AIzaSyAQ5NOVTp3LuGQZTb3RC_RREpTe3JGpvdg"
youtube = build("youtube", "v3", developerKey=api_key)


#get relatedChannel with video_id
id_dict = {}
error_video_id = []
error_related_id = [] 
for video_id, types in video_ids.items():
    try:
        channel = yt_search_relatedChannel_withVideoId(video_id, api_key)
        channel_idList = channel.get_onlyChannelId()
        for item in channel_idList:
            id_dict[item] = types
    except:
        error_video_id.append(video_id)


filename = '/Users/seanyoo/Desktop/knn_project2.0/json/new1.0.json'
for url, type in id_dict.items():
    trial = yt_channel_vid_statistic(url, api_key, youtube, my_categ=str(type))
    trial.updateJson(filename) 

