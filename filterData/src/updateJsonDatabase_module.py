import json

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

#commdbing on all file1_path 
file1_path = "/Users/seanyoo/Desktop/yt_sql_database/json/yt_channelVideo_stats-Database.json"

#things to put on file1_path
file2_path = "/Users/seanyoo/Desktop/yt_sql_database/json/yt_channelVideo_stats0.0.json"
combine_json_files(file1_path, file2_path)