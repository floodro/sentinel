import re
import time
import csv
import pickle
import pandas as pd
import tweepy as tw
import matplotlib.pyplot as plt
import preprocessor as p

from textblob import TextBlob
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from wordcloud import WordCloud

api = None
dataFrame = pd.DataFrame()

def clean_tweet(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text) #remove mentions
    text = re.sub(r'#', '', text) #removing the '#' symbol
    text = re.sub(r'RT[\s]+', '', text) #remove the RT 
    text = re.sub(r'https?:\/\/\S+', '', text) #remove the hyperlink
    text = re.sub('<[^>]*>', '', text) #remove html markups
    text = re.sub('[\W]+', ' ', text.lower()) #make lowercase

    return text

def remove_punctuation(words):
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', (word))
        if new_word != '':
            new_words.append(new_word)
    return new_words

def get_twitter_data():
    word_library = ['kill', 'die', 'life', 'hurt', 'suicide', 'sleep', 'tired', 'done', 'save me', 'help me', 'fuck my life']
    data_to_collect = 1000
    since_when = '2024-01-01'
    counter = 0
    tweet_counter = 1

    with open('tweet_data_only.csv', 'w') as file:
        tweet_only = csv.writer(file)
        tweet_only.writerow(['Tweet'])

        for tweet in tw.Cursor(api.search_tweets, word_library[0], lang='en', since=since_when).items(data_to_collect):
            tweet_only.writerow([tweet.text.replace('\n', ' ').encode('utf-8')])
            time.sleep(2)
            counter += 1

            print("Data stored - " + str(tweet_counter))
            tweet_counter += 1

            if tweet_counter == 1000:
                is_finished = True

def remove_randoms():
    global dataFrame
    dataFrame['Tweet'] = dataFrame['Tweet'].str.replace('b', '')
    dataFrame['Tweet'] = dataFrame['Tweet'].str.replace('xat', '')
    dataFrame['Tweet'] = dataFrame['Tweet'].str.replace('xe2', '')

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

#Create a function to get the polarity of a text (tells how positive or negative a text is)
def getPolarity(text):
    return TextBlob(text).sentiment.polarity

def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

API_KEY = '1mvSADxXWmhSInt3lZM54Vrb7'
API_SECRET = 'sRwNjMHuV2ly0GQ9se1W9Sum1ko0d5l9gXloI8O6qiCBcryCsi'

ACCESS_KEY = '2348050974-iZAqAmOJGbwOs9d1VKUbVZrtVDpODshwQdyj4tX'
ACCESS_SECRET = 'WQxwRxCu6fi43CujfnXL2U2CvhoixYhej3WQ4IrJsbZmS'

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAABkxlgEAAAAAi4M6WU1%2FHtu9Ou1viaWMtNzetw4%3Dsmf9SoFajl54N15vZwF5oiN8PRYv514fTwYaXZeJ0SckfeqjI2'

auth = tw.OAuthHandler(API_KEY, API_SECRET, ACCESS_KEY, ACCESS_SECRET)
api = tw.API(auth)

is_finished = False
get_twitter_data()
'''dataFrame = pd.read_csv('tweet_data_only.csv')
dataFrame['Tweet'] = dataFrame['Tweet'].apply(clean_tweet)
remove_randoms()
dataFrame.to_csv('CLEANED_tweet_data_only.csv')

dataFrame['Subjectivity'] = dataFrame['Tweet'].apply(getSubjectivity)
dataFrame['Polarity'] = dataFrame['Tweet'].apply(getPolarity)

print(dataFrame)

allWords = ''.join([twts for twts in dataFrame['Tweet']])
wordCloud = WordCloud(width = 600, height = 600, random_state = 21, max_font_size = 150).generate(allWords)

plt.title('Word Cloud')
plt.imshow(wordCloud, interpolation = 'bilinear')
plt.axis('off')
plt.show()

dataFrame['Analysis'] = dataFrame['Polarity'].apply(getAnalysis)

j = 1
print('Printing positive tweets: \n')
sortedDF = dataFrame.sort_values(by=['Polarity']) #sort the tweets in ascending order

for i in range(0, sortedDF.shape[0]):
    if (sortedDF['Analysis'][i] == 'Positive'):
        print(str(j) + ')' + sortedDF['Tweet'][i])
        print()
        j = j + 1

j = 1
print('Printing negative tweets: \n')
sortedDF = dataFrame.sort_values(by=['Polarity'], ascending=False) #sort the tweets in descending order

for i in range(0, sortedDF.shape[0]):
    if (sortedDF['Analysis'][i] == 'Negative'):
        print(str(j) + ')' + sortedDF['Tweet'][i])
        print()
        j = j + 1

plt.figure(figsize=(8,6))

for i in range (0, dataFrame.shape[0]):
    plt.scatter(dataFrame['Polarity'][i], dataFrame['Subjectivity'][i], color = 'Blue')

plt.title('Tweet Sentiment Analysis')
plt.xlabel('Polarity')
plt.ylabel('Subjectivity')
plt.show()

positive_tweets = dataFrame[dataFrame.Analysis == 'Positive']
positive_tweets = positive_tweets['Tweet']
print(positive_tweets)

negative_tweets = dataFrame[dataFrame.Analysis == 'Positive']
negative_tweets = negative_tweets['Tweet']
print(negative_tweets)
print(dataFrame['Analysis'].value_counts())

plt.title('Tweet Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
dataFrame['Analysis'].value_counts().plot(kind = 'bar')
plt.show()'''
