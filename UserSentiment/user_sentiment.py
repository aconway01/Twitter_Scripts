import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, date, time, timedelta

from tweepy import Cursor
from collections import Counter
import argparse

consumer_key = ''
consumer_secret = ''

access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

def parse(username):

    item = api.get_user(username)

    handle =  item.name
    screen_name = item.screen_name
    account_des = item.description
    statuses_count = str(item.statuses_count)
    friends_count =  str(item.friends_count)
    followers_count =  str(item.followers_count)

    tweets_cnt = item.statuses_count
    account_created_date = item.created_at
    delta = datetime.utcnow() - account_created_date
    account_age_days = delta.days

    hashtags = []
    mentions = []
    tweets = []
    tweet_count = 0
    num_days = 30
    end_date = datetime.utcnow() - timedelta(days=num_days)
    for status in Cursor(api.user_timeline, id=username).items():
        tweet_count += 1
        tweets.append(status.text)
        if hasattr(status, "entities"):
            entities = status.entities
            if "hashtags" in entities:
                for ent in entities["hashtags"]:
                    if ent is not None:
                        if "text" in ent:
                            hashtag = ent["text"]
                            if hashtag is not None:
                                hashtags.append(hashtag)
            if "user_mentions" in entities:
                for ent in entities["user_mentions"]:
                    if ent is not None:
                        if "screen_name" in ent:
                            name = ent["screen_name"]
                            if name is not None:
                                mentions.append(name)
        if status.created_at < end_date:
            break

    analyzer = SentimentIntensityAnalyzer()
    threshold = 0.5
    avg_sentiment = 0.0
    pos = 0
    neg = 0
    neutral = 0
 
    for tweet in tweets:
        print(tweet)
        vs = analyzer.polarity_scores(tweet)
        comp_val = vs['compound']
        avg_sentiment += (comp_val/len(tweets))
        if comp_val >= threshold:
            print('positive')
            pos += 1
        elif comp_val <= -1*threshold:
            print('negative')
            neg += 1
        else:
            print('neutral')
            neutral += 1
        print()

    print()
    print("name: " + handle)
    print("screen_name: " + screen_name)
    print("description: " + account_des)
    print("statuses_count: " + str(statuses_count))
    print("friends_count: " + str(friends_count))
    print("followers_count: " + str(followers_count))
    print("account age (in days): " + str(account_age_days))
    if account_age_days > 0:
        print("average tweets per day: ",float(tweets_cnt)/float(account_age_days))

    print()
    print("most mentioned twitter users: ")
    for item,count in Counter(mentions).most_common(10):
        print(item + "\t" + str(count))

    print()
    print("most used hashtags: ")
    for item,count in Counter(hashtags).most_common(10):
        print(item + "\t" + str(count))

    print()
    print("Processed " + str(tweet_count) + " tweets.")

    print()
    print("Average sentiment: ",avg_sentiment)
    if avg_sentiment >= threshold:
        print("Mostly positive")
    elif avg_sentiment <= -1*threshold:
        print("Mostly negative")
    else:
        print("Mostly neutral")

    print()
    print("Percent Positive: ",(pos/len(tweets))*100)
    print("Percent Negative: ",(neg/len(tweets))*100)
    print("Percent Neutral: ",(neutral/len(tweets))*100)

if __name__=="__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('username',help = '')
    args = argparser.parse_args()
    username = args.username
    print("Fetching data for %s"%(username))
    parse(username)
