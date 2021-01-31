from textblob import TextBlob
from wordcloud import WordCloud
from tqdm import tqdm 
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer

import pandas as pd
import tweepy as tw 
import matplotlib.pyplot as plt
import preprocessor as p
import nltk
import re, time, csv, sys, pickle 

nltk.download
nltk.download('wordnet')
nltk.download('stopwords')

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
    word_library = ['kill', 'die', 'life', 'hurt', 'suicide', 'sleep', 'tired', 'done', 'save me']
    data_to_collect = 100
    since_when = '2020-11-07'
    counter = 0
    tweet_counter = 1
        
    with open('tweet_data_only.csv', 'w') as file:
        tweet_only = csv.writer(file)
        tweet_only.writerow(['Tweet'])

        for tweet in tw.Cursor(api.search, word_library[0], lang='en', since=since_when).items(data_to_collect):
            tweet_only.writerow([tweet.text.replace('\n', ' ').encode('utf-8')])
            #time.sleep(2)
            counter += 1

            print("Data stored - " + str(tweet_counter))
            tweet_counter += 1

            if tweet_counter == 100:
                is_finished = True

def remove_randoms():
    dataFrame['Tweet'] = dataFrame['Tweet'].str.replace('b', '')
    dataFrame['Tweet'] = dataFrame['Tweet'].str.replace('xat', '')
    dataFrame['Tweet'] = dataFrame['Tweet'].str.replace('xe2', '')
    dataFrame['Tweet'] = dataFrame['Tweet'].str.replace('x80', '')
    dataFrame['Tweet'] = dataFrame['Tweet'].str.replace('x9f', '')
    dataFrame['Tweet'] = dataFrame['Tweet'].str.replace('xf0', '')
    dataFrame['Tweet'] = dataFrame['Tweet'].str.replace('x98', '')
    dataFrame['Tweet'] = dataFrame['Tweet'].str.replace('xa6', '')
    dataFrame['Tweet'] = dataFrame['Tweet'].str.replace('_', '')

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

api_key = 'your twitter api key' 
api_secret = 'your twitter api secret key'

access_key = 'your twitter access key'
access_secret = 'your twitter access secret key'

bearer_key = 'AAAAAAAAAAAAAAAAAAAAAD%2FRJQEAAAAAS1ePMvntMjtEoDbe%2Fj%2FSCtYB8Ds%3D9skdWCqn9n5Qm3J39XXfDylFt8S9127HiSBIWjeLa46uTydcmS'

auth = tw.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_key, access_secret)
api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

is_finished = False

dataFrame = pd.read_csv('tweet_data_only.csv')
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
plt.show()
