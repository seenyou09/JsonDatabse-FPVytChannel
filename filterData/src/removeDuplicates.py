from filterData.src.removeDuplicates_module import CleanNewExcelInputForJsonDB
import pandas as pd 


'''
1. Remove the duplicates from the main database and the new excel input
2. Manually check to see if the youtube link is adequate 
'''


database_jsonFile = '/Users/seanyoo/Desktop/buildingJsonDatabse-FPVpilotsYT/_final_Database/yt_channelVideo_stats-Database.json'
raw_input_xlsx = '/Users/seanyoo/Desktop/yt_sql_database/input_xlsx/new1.0-contactedbefore.xlsx'
processed_xlsx = CleanNewExcelInputForJsonDB(database_jsonFile, raw_input_xlsx)
processed_xlsx_dict = processed_xlsx.removeduplicate()

processed_xlsx_file_name = "processed-contactedbefore.xlsx"
df = pd.DataFrame(processed_xlsx_dict.items(), columns=['Channel_id', 'Category'])
df.to_excel(processed_xlsx_file_name, index=False)


