'''
1. We want to update te load the excel json form 
2. write the json file input into the Databse json file 

How to Use properly
1. Create a new Json file including {}
2. change the processed_xlsx_file_name from the output_xlsx file to the new channels you want to add

'''
import json
import pandas as pd
from googleapiclient.discovery import build
from _youtubeAPI.videoStatsdicTojson import yt_channel_vid_statistic
api_key = 'AIzaSyBRyZE6fmuOE-iuDsicVokpEMbJv_ZVe1Y'
youtube = build("youtube", "v3", developerKey=api_key)

#Database jsonfile 
database_jsonFile = '/Users/seanyoo/Desktop/buildingJsonDatabse-FPVpilotsYT/_final_Database/yt_channelVideo_stats-Database.json'

# Read the processed Excel 'file and convert it to a dictionary
processed_xlsx_file_name = '/Users/seanyoo/Desktop/yt_sql_database/output_xlsx/processed-contactedbefore.xlsx'
df = pd.read_excel(processed_xlsx_file_name)
channel_id_dict = dict(zip(df['Channel_id'], df['Category']))

# Create a new JSON file and input the Excel file data
error_list = []
processed_xlsx_json = '/Users/seanyoo/Desktop/yt_sql_database/json/contactedbefore.json'
for url, type in channel_id_dict.items():
    try: 
        url = "https://www.youtube.com/channel/" + url
        trial = yt_channel_vid_statistic(url, api_key, youtube, my_categ=str(type))
        trial.updateJson(processed_xlsx_json)
    except:
        error_list.append(url)




#Need Updating 

# Function to read and load JSON data from a file
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to write JSON data to a file
def write_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def combine_json_files(file1_path, file2_path):
    # Step 1: Read and parse data from the first JSON file
    data_from_file1 = read_json_file(file1_path)

    # Step 2: Read and parse data from the second JSON file
    data_from_file2 = read_json_file(file2_path)

    # Step 3: Merge the data from both files into one
    # For example, let's assume both files contain dictionaries
    combined_data = {**data_from_file1, **data_from_file2}

    # Step 4: Write the combined data back to the first JSON file
    write_json_file(file1_path, combined_data)

# Usage:
combine_json_files(database_jsonFile, processed_xlsx_json)