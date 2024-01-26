# YouTube Channel Explorer: Enhancing FPV Drone YouTube Channel Discovery

## Description
---

The YouTube Channel Explorer is an innovative project designed to continuously identify, extract, and categorize new FPV drone YouTube channels for inclusion in our comprehensive JSON database. Leveraging the YouTube API and advanced data analysis techniques, this tool streamlines the discovery and organization of drone-related content, catering to enthusiasts and professionals alike.

## Workflow Overview
---

### Data Extraction (`_youtubeAPI`)
---
- **Module Functionality**: Utilizes a custom Python module to interact with the YouTube API, retrieving detailed statistics about YouTube channels and videos.
- **Output**: Converts the retrieved information into JSON files, laying the groundwork for the creation of the final JSON database.

### Data Transformation (`extractData`)
---
- **Process**: Extracts a list of YouTube channels based on specified key terms or channel IDs, initially generating an Excel file.
- **Conversion**: Employs the `converExceltoJson` module to transform the Excel (CSV) output into JSON format, improving data readability and organization for further analysis.

### Categorization Model Training (`categorizeData`)
---
- **Training**: Leverages a machine learning model (`trainTestModel`) trained on a database of previously sponsored YouTube channels.
- **Objective**: To categorize new YouTube channels into one of four predefined categories:
  - **No Related**: Channels outside the specified categories.
  - **Cinematic**: Channels focused on cinematic content creation.
  - **Drone Review**: Channels reviewing drone technology.
  - **Freestyle/Racing**: Channels showcasing drone racing and freestyle flying.

### Data Filtering and Manual Verification (`filterData`)
---
- **Duplication Removal**: Implements a process to identify and remove duplicate entries, ensuring database accuracy.
- **Manual Review**: Involves a manual verification step to assess the accuracy of the categorization process, guaranteeing that the database reflects true channel content.

## Features
---

- **Advanced Data Extraction**: Customized YouTube API module for comprehensive data retrieval.
- **Efficient Data Transformation**: Streamlined conversion from CSV to JSON, enhancing data usability.
- **Intelligent Categorization**: Automated channel categorization based on content analysis, supported by machine learning.
- **Data Integrity**: Rigorous filtering and verification processes to maintain an up-to-date and reliable database.

Embark on a journey of discovery with the YouTube Channel Explorer, and uncover the vast world of FPV drone YouTube channels. Our project not only facilitates the exploration of similar channels but also showcases proficiency in data analysis and application of the YouTube API for dynamic content categorization.
