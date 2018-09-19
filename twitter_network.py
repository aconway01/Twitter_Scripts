import tweepy
import pandas as pd
from datetime import datetime, date, time, timedelta
import math

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

def logistic(x):
    return 100*round((1/(1+math.e**(-1*(x)))),4)

def parse(username):
    item = api.get_user(username)

    user = item.screen_name
    tweets = item.statuses_count
    account_created_date = item.created_at
    delta = datetime.utcnow() - account_created_date
    account_age_days = delta.days
    avg_tweets_day = 0.0
    beta = 0.0
    if account_age_days > 0:
        avg_tweets_day = float(tweets)/float(account_age_days)
        beta = 1/avg_tweets_day

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
            if "user_mentions" in entities:
                for ent in entities["user_mentions"]:
                    if ent is not None:
                        if "screen_name" in ent:
                            name = ent["screen_name"]
                            if name is not None:
                                mentions.append(name)
        if tweet_count == 200:
            break

    top_mentions = []
    cnt = 0
    for item,count in Counter(mentions).most_common(10):
        if cnt < 5:
            top_mentions.append([item,count])

    return user, beta, top_mentions

if __name__=="__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('username',help = '')
    args = argparser.parse_args()
    username = args.username
    print("Fetching data for %s"%(username))
    # [[username,alpha],[top_mentions (users and counts)]]
    rootName, rootBeta, rootMentions = parse(username)

    names = []
    names.append(rootName)
    betas = []
    betas.append(rootBeta)
    mentions = []
    mentions.append(rootMentions)
    beta_mentions = []
    root_beta_mentions = [[mentions[0][i][0],logistic(mentions[0][i][1]*betas[0])] for i in range(len(mentions[0]))]
    beta_mentions.append(root_beta_mentions)

    for user in rootMentions:
        try:
            name,beta,mention = parse(user[0])
            names.append(name)
            betas.append(beta)
            mentions.append(mention)
            beta_mention = [[mention[i][0],logistic(mention[i][1]*beta)] for i in range(len(mention))]
            beta_mentions.append(beta_mention)
        except:
            print("Err: User profile private")

    for i in range(len(names)):
        print(names[i])
        print(beta_mentions[i])
        print()

