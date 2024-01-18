import json 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier

class trainTestModel:
    def __init__(self, filepath):
        self.jsonfile = filepath
        self.f_dict = self.convertJson_Dict()
        self.df = self.cleanConvertPdforTrainTest()

        
    def convertJson_Dict(self):
        with open(self.jsonfile , 'r') as file:
            data_dict = json.load(file)
        # Iterate over dictionary items
        i = 0 
        self.f_dict = {}
        for key,value in data_dict.items():
            channel_name = value["Channel_name"]
            channel_id = value["Channel_id"]
            titles_list = []
            descriptions_list = []
            for item in value["Video_statistic"]:
                titles_list.append(item["title"])
                title = ''.join(titles_list)
                descriptions_list.append(item["description"])
                descriptions = ''.join(descriptions_list)
            channel_stats = value["Channel_Statistic"]
            categories = channel_stats["Categories"]
            keywords = channel_stats["Keywords"]
            manual_category =channel_stats["Manual_category"]
            self.f_dict[channel_id] = channel_name, title, descriptions, categories, keywords, manual_category  
        return self.f_dict
    
    
    def cleanConvertPdforTrainTest(self):
        description_dict = {} 
        for keys, values in self.f_dict.items():
            description = values[2]
            channel_name = values[0]
            title = values[1]
            final = description + channel_name + title
            category = values[5]
            category = category.strip()
            if category == "No Related":
                category = 0
            elif category == "Cinematic":
                category = 1
            elif category == "Drone Review":
                category = 2
            elif category == "Freestyle/Racing":
                category = 3
            description_dict[keys] = {'ChannelId': keys,
                                      'ChannelName': channel_name,
                                    'Description': final,
                                    'Category': category
                                    }
            
        self.df = pd.DataFrame(description_dict)
        self.df = self.df.transpose() 
        # Convert 'Category' column to integer type
        try:
            self.df['Category'] = self.df['Category'].astype(int)
        except:
            pass
        return self.df
    
    def trainTestSplit(self):
        X_train, X_test, y_train, y_test = train_test_split(
        self.df.Description, 
        self.df.Category, 
        test_size=0.2, # 20% samples will go to test dataset
        random_state=2022,
        stratify=self.df.Category)
        
        #1. create a pipeline object
        clf = Pipeline([
            ('vectorizer_tfidf',TfidfVectorizer()),     
            ('Random Forest', RandomForestClassifier())         
        ])

        #2. fit with X_train and y_train
        clf.fit(X_train, y_train)


        #3. get the predictions for X_test and store it in y_pred
        y_pred = clf.predict(X_test)


        #4. print the classfication report
        report = classification_report(y_test, y_pred)
        
        return report
    
    def predict_newdataset(self, trainClf):
        new_descriptions = self.df["Description"].tolist()
        y_pred = trainClf.predict(new_descriptions)
        pred_df = pd.DataFrame(columns=["Channel_id", 'Channel_name', "Category"])
        count = 0 
        for category in y_pred:
            if category == 0:
                category_name = "No Related"
            elif category == 1:
                category_name = "Cinematic"
            elif category == 2:
                category_name = "Drone Review"
            elif category == 3:
                category_name = "Freestyle/Racing"
            else:
                category_name = ""
            
            channel_id = self.df['ChannelId'][count]
            channel_name = self.df['ChannelName'][count]
            pred_df.at[count, 'Channel_id'] = channel_id
            pred_df.at[count, 'Channel_name'] = channel_name
            pred_df.at[count, 'Category'] = category_name
            count += 1

        return pred_df


        
    

if __name__ == "__main__":
    #Train the model with the database we have
    filepath = '/Users/seanyoo/Desktop/knn_project2.0/json-database/yt_channelVideo_stats-Database.json'
    trial = trainTestModel(filepath)
    clfTrainedwithDatabase = trial.trainTestSplit()

    #Use the trained model on with new sample to categorize whether it is not related, cinematic, Freestyle, Drone Review
    input_filepath = '/Users/seanyoo/Desktop/knn_project2.0/json-output/yt_channelVideo_stats_contactedBefore.json'
    sample = trainTestModel(input_filepath)
    new_inputdf = sample.predict_newdataset(clfTrainedwithDatabase)
    
    
    #output the pandas to excel 
    excel_name ='20230721newinput1.0.xlsx'
    new_inputdf.to_excel(excel_name, index=False)
