# Sentinel: Suicidal Tweet Detection

## Overview
Sentinel is a sentiment analysis project designed to detect potential suicidal ideation in tweets. The project leverages natural language processing (NLP) techniques to clean, analyze, and visualize tweet data. The dataset used is sourced from Kaggle, and the cleaned data is stored in an SQLite database for further analysis.

## Features
- **Data Cleaning**: Removes mentions, hashtags, retweets, links, and special characters.
- **Sentiment Analysis**: Uses TextBlob to calculate subjectivity and polarity of tweets.
- **Database Storage**: Stores cleaned tweets and analysis results in an SQLite database.
- **Visualization**:
  - Generates a word cloud of frequently used words.
  - Displays a sentiment distribution bar chart.
- **Sample Tweet Extraction**: Displays a few positive and negative tweets based on sentiment analysis.

## Setup & Execution
### Create a Virtual Environment
Before installing dependencies, it is recommended to create a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### Install Dependencies
To run this project, install the following Python libraries:
```
pip install -r requirements.txt
```

## Execution
1. Download the dataset from Kaggle.
2. Run the script to clean, analyze, and store tweets.
3. View the visualizations and sentiment analysis results.
4. The cleaned data is stored in `tweets.db` under the table `cleaned_tweets`.

Run the script:
```
python sentinel.py
```

## Database Schema
The cleaned tweet data is stored in an SQLite database with the following schema:
```
CREATE TABLE cleaned_tweets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Tweet TEXT,
    Subjectivity REAL,
    Polarity REAL,
    Analysis TEXT
);
```

## Evaluation
To improve accuracy, the sentiment analysis can be cross-validated using alternative methods such as VADER sentiment analysis or machine learning-based classifiers.

## Future Enhancements
- Implement VADER sentiment analysis for comparison.
- Train a machine learning model for more accurate classification.
- Deploy the project as a web application for real-time analysis.

## Disclaimer
This project is for research and educational purposes only. It is not intended to replace professional mental health support. If you or someone you know is struggling, please seek help from a qualified professional.

## License
This project is open-source and licensed under the MIT License.

