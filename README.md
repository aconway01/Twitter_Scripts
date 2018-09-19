# twitter_network
Python script to analyze Twitter user relationships using username mentions, mention counts, and average tweets per day.

usage: twitter_network.py [-h] username

User relationship strength is measured by user mentions multiplied by beta, where beta equals 1/average tweets per day.

This value is then normalized using a logistic function.

Usernames from the list of initial mentions are then analyzed using the same approach.

The 200 most recent tweets from each account are used for user mention counts.

NOTE: Must include consumer key, consumer secret,access token, and access token secret from an active twitter developer account
