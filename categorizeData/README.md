
# YouTube Channel Explorer: Discover Similar Channels with Python and YouTube API

### Data Extraction:
---
Extracts data from YouTube channels using the YouTube API module that I customized, generating CSV files as output.

### Data Transformation:
----
Converts CSV files to JSON format using the converExceltoJson module, enhancing data readability and organization.

### Categorization Model Training:
----
Trains the machine learning model (trainTestModel) on a database of previously sponsored YouTube channels. The model learns to categorize new channels into predefined content categories.

### Categorization Process:
----
Applies the trained model to categorize new YouTube channels into one of the four predefined categories: "No Related," "Cinematic," "Drone Review," and "Freestyle/Racing."

### Manual Verification:
----
Manually reviews a sample of categorized channels to validate the accuracy of the model's predictions.
