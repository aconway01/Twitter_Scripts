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

def search(username):

    users = api.search_users(username)

    for user in users:
        print("name: " + user.name)
        print("screen_name: " + user.screen_name)
        print("description: " + user.description)
        print("statuses_count: " + str(user.statuses_count))
        print("friends_count: " + str(user.friends_count))
        print("followers_count: " + str(user.followers_count))
        
        print()

if __name__=="__main__":
    username = str(input("Enter user search: "))
    print("Fetching data for %s"%(username))
    userinfo = search(username)

