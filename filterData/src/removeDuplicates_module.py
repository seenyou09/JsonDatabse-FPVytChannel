import pandas as pd
import json

class CleanNewExcelInputForJsonDB:

    def __init__(self, jsonfile, input_excel):
        self.jsonfile = jsonfile
        self.input_excel = input_excel
        self.input_dict = self.convertExcel_Dict()
        self.f_dict = self.convertJson_Dict()
        self.uniqueInput = self.removeduplicate()

    def convertExcel_Dict(self):
        df = pd.read_excel(self.input_excel)
        input_dict = df.set_index('Channel_id')['Category'].to_dict()
        return input_dict

    def convertJson_Dict(self):
        with open(self.jsonfile, 'r') as file:
            data_dict = json.load(file)

        f_dict = {}
        for key, value in data_dict.items():
            channel_name = value["Channel_name"]
            channel_id = value["Channel_id"]
            channel_stats = value["Channel_Statistic"]
            subscribers = channel_stats["Subscribers"]
            manual_category = channel_stats["Manual_category"]
            f_dict[channel_id] = (channel_name, subscribers, manual_category)
        return f_dict

    def removeduplicate(self):
        keys_set1 = set(self.input_dict.keys())
        keys_set2 = set(self.f_dict.keys())

        duplicate_keys = keys_set1.intersection(keys_set2)

        # Remove duplicate keys from the input_dict
        for key in duplicate_keys:
            self.input_dict.pop(key)

        return self.input_dict

if __name__ == '__main__':
    jsonfile = '/Users/seanyoo/Desktop/yt_sql_database/json/yt_channelVideo_stats-Database.json'
    input_excel = '/Users/seanyoo/Desktop/yt_sql_database/input_xlsx/yt_channelVideo_stats_contactedBefore.xlsx'
    trial = CleanNewExcelInputForJsonDB(jsonfile, input_excel)
    uniqueinput = trial.removeduplicate()

    file_name = "yt_channelVideo_stats_contactedBefore.xlsx"
    df = pd.DataFrame(uniqueinput.items(), columns=['Channel_id', 'Category'])
    df.to_excel(file_name, index=False)

