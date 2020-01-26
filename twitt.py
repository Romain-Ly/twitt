#!/usr/bin/env python3
# encoding=utf8
"""
    Script for getting tweets
"""

import os
import argparse
import configparser
import datetime as date
import re
import itertools
import collections

import tweepy as tw
import pandas as pd


def clean_tweet(txt):
    """
    - Replace URLs found in a text string with nothing
      (i.e. it will remove the URL from the string).
    - Keep hashtag.
    - Lower case
    """
    tmp = re.sub(r"([^#0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split()
    return [txt.lower() for txt in tmp]


def get_tweets(args, cfg):
    """
    Use python api to get tweets.
    """
    twcfg = cfg['twitter']
    auth = tw.OAuthHandler(twcfg['CONSUMER_KEY'], twcfg['CONSUMER_SECRET'])
    auth.set_access_token(twcfg['ACCESS_TOKEN'], twcfg['ACCESS_TOKEN_SECRET'])
    api = tw.API(auth, wait_on_rate_limit=True)

    search_words = "#metal"
    date_since = date.date.today() - date.timedelta(days=args.days)
    date_since = date_since.strftime("%Y-%m-%d")

    # Collect tweets
    tweets = tw.Cursor(api.search, q=search_words, lang="en",
                       since=date_since).items(args.nb_tweet)
    return tweets

# region : parse args

def parseargs():
    """
    parse script arguments
    """
    parser = argparse.ArgumentParser(description='Tweet Metal.')
    parser.add_argument('-n',
                        '--tweet',
                        dest='nb_tweet',
                        type=int,
                        default=5,
                        help='number of tweets')
    parser.add_argument('-f',
                        '--cfg',
                        dest='cfg',
                        type=str,
                        default='twitter.cfg',
                        help='twitter configuration')
    parser.add_argument('-d',
                        '--days',
                        dest='days',
                        type=int,
                        default=7,
                        help='days since twits')
    args = parser.parse_args()
    return args

# endregion

def main():
    """ main function """
    args = parseargs()
    config = configparser.ConfigParser()
    config.read(args.cfg)

    tweets = get_tweets(args, config)
    # Beware tweet.text is a kind of generator. You cannot call it twice.
    tws = [clean_tweet(tweet.text) for tweet in tweets]
    print(tws)


if __name__ == "__main__":
    # execute only if run as a script
    main()
