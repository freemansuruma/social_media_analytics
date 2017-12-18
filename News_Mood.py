
# coding: utf-8

# In[10]:


#Import dependicies to use
import tweepy
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# In[11]:


#Analyzer for sentiment analysis
analyzer = SentimentIntensityAnalyzer()


# In[12]:


#Authorize twitter account
consumer_key = "Wr8HVqu6PPPotwB3aYLxI2dKg"
consumer_secret = "fr1Htp7OjsMdxleOf5R3LhSTEbU0PpZvNrrm1BGODQk3s5b1TS"
access_token = "3029074810-5udMvQvQqmUFkhRk5gTuMhXlkyzyAnPnQiOa9JQ"
access_token_secret = "s19MHBizwdEumNHhKn5yiVfVM38zeWVx5x83MtA49Rn2m"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


# In[13]:


#Set the name of the twitter accounts you would like to analyze and set empty dictionary to hold compound sentiment data
target_accounts = ('@BBC','@CNN','@CBS','@FoxNews','@nytimes')
sentiment_list = {}


# In[14]:


#Create dataframe to hold the tweet data and export to excel
media_sentiment_df = pd.DataFrame()
media_sentiment_df['Account'] = ''
media_sentiment_df['Tweet text'] = ''
media_sentiment_df['Date'] = ''
media_sentiment_df['Positive Score'] = ''
media_sentiment_df['Negative Score'] = ''
media_sentiment_df['Neutral Score'] = ''
media_sentiment_df['Compound Score'] = ''
media_sentiment_df


# In[18]:


#Fetch data from twitter and loop through the text to find the sentiment for each account and store in a list
for account in target_accounts:
    compound_list = []
    negative_list = []
    positive_list = []
    neutral_list = []
    date_list = []
    text_list = []
    name_list = []
    public_tweets = api.user_timeline(account,count=100)
    for tweet in public_tweets:
        text = tweet['text']
        date = tweet['created_at']
        user = tweet['user']['name']
        
        compound = analyzer.polarity_scores(text)["compound"]
        neg = analyzer.polarity_scores(text)['neg']
        pos = analyzer.polarity_scores(text)['pos']
        neu = analyzer.polarity_scores(text)['neu']
        compound_list.append(compound)
        negative_list.append(neg)
        positive_list.append(pos)
        neutral_list.append(neu)
        date_list.append(date)
        text_list.append(text)
        name_list.append(user)
        sentiment_list[account] = compound_list
        


# In[19]:

#Populate dataframe with information gathered from twitter
media_sentiment_df['Account'] = name_list
media_sentiment_df['Tweet text'] = text_list
media_sentiment_df['Date'] = date_list
media_sentiment_df['Positive Score'] = positive_list
media_sentiment_df['Negative Score'] = negative_list
media_sentiment_df['Neutral Score'] = neutral_list
media_sentiment_df['Compound Score'] = compound_list
media_sentiment_df.head()


# In[23]:

#Export dataframe to csv file
media_sentiment_df.to_csv('NewsSentiment.csv',index=False,header=True)


# In[20]:

#Create separate dataframe to hold compound scores
sentiments_df = pd.DataFrame(sentiment_list)
sentiments_df.head(10)


# In[21]:

#Plot the compound score for each tweet for each account
bbc, = plt.plot(np.arange(len(sentiments_df)),sentiments_df['@BBC'],marker="o", linewidth=0,alpha=0.8,color='r',label='BBC')
cbs, = plt.plot(np.arange(len(sentiments_df)),sentiments_df['@CBS'],marker="o", linewidth=0,alpha=0.8,color='b',label='CBS')
cnn, = plt.plot(np.arange(len(sentiments_df)),sentiments_df['@CNN'],marker="o", linewidth=0,alpha=0.8,color='m',label='CNN')
fox, = plt.plot(np.arange(len(sentiments_df)),sentiments_df['@FoxNews'],marker="o", linewidth=0,alpha=0.8,color='g',label='FOX')
nyt, = plt.plot(np.arange(len(sentiments_df)),sentiments_df['@nytimes'],marker="o", linewidth=0,alpha=0.8,color='y',label='NYT')

plt.grid(True)
plt.legend(handles=[bbc,cbs,cnn,fox,nyt],bbox_to_anchor=(1, 1))
plt.title('Sentiment Analysis of News Outlets')
plt.xlabel('Tweets Ago')
plt.ylabel('Tweet Polarity')
plt.savefig('news_media_sentiment.png')
plt.show()


# In[22]:

#Plot bar chart showing average compound score for each account
compound_average = [sentiments_df['@BBC'].mean(),sentiments_df['@CBS'].mean(),sentiments_df['@CNN'].mean(),
                    sentiments_df['@FoxNews'].mean(),sentiments_df['@nytimes'].mean()]

objects = ('BBC','CBS','CNN','FOX','NYT')
axis = np.arange(len(objects))
chart = plt.bar(axis,compound_average,align='center',alpha=0.5)
chart[0].set_color('r')
chart[1].set_color('b')
chart[2].set_color('g')
chart[3].set_color('yellow')
chart[4].set_color('k')
plt.xticks(axis,objects)
plt.ylim(-0.2,0.5)
plt.title('Overall Media Sentiment bases on Twitter')
plt.ylabel('Tweet Polarity')
plt.savefig('media_sentiment_barchart.png')
plt.show()

