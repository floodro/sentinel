import sqlite3
import re
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from wordcloud import WordCloud

db_path = "database/dataset.db"
conn = sqlite3.connect(db_path)

# Load data into a Pandas DataFrame
query = "SELECT Tweet, Suicide FROM tweets;"
dataFrame = pd.read_sql_query(query, conn)

# Close the connection
conn.close()

def clean_tweet(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)  # Remove mentions
    text = re.sub(r'#', '', text)  # Remove hashtags
    text = re.sub(r'RT\s+', '', text)  # Remove retweets
    text = re.sub(r'https?:\/\/\S+', '', text)  # Remove links
    text = re.sub('<[^>]*>', '', text)  # Remove HTML tags
    return text

dataFrame['Tweet'] = dataFrame['Tweet'].apply(clean_tweet)

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
    return TextBlob(text).sentiment.polarity

def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

dataFrame['Subjectivity'] = dataFrame['Tweet'].apply(getSubjectivity)
dataFrame['Polarity'] = dataFrame['Tweet'].apply(getPolarity)
dataFrame['Analysis'] = dataFrame['Polarity'].apply(getAnalysis)

# Connect to SQLite database and save cleaned data
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a new table for cleaned tweets
cursor.execute("""
CREATE TABLE IF NOT EXISTS cleaned_tweets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Tweet TEXT,
    Subjectivity REAL,
    Polarity REAL,
    Analysis TEXT
)
""")

# Insert cleaned data into the new table
dataFrame.to_sql('cleaned_tweets', conn, if_exists='replace', index=False)

# Commit and close connection
conn.commit()
conn.close()

# Word cloud visualization
allWords = ' '.join([twts for twts in dataFrame['Tweet']])
wordCloud = WordCloud(width=600, height=600, random_state=21, max_font_size=150).generate(allWords)
plt.title('Word Cloud')
plt.imshow(wordCloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# Sentiment distribution
dataFrame['Analysis'].value_counts().plot(kind='bar', title='Tweet Sentiment Analysis', xlabel='Sentiment', ylabel='Counts')
plt.show()

print("Positive Tweets:\n", dataFrame[dataFrame['Analysis'] == 'Positive']['Tweet'].head())
print("Negative Tweets:\n", dataFrame[dataFrame['Analysis'] == 'Negative']['Tweet'].head())
