import os

import praw

from mongo_helpers.mongo_dto import RedditScrapperMongo
from utils.helpers import extract_crypto_symbol, convert_unix_timestamp_to_date_time


class RedditScrapper(object):
    reddit_instance = None
    sub_reddit_instance = None
    reddit_topic = ''
    reddit_topic_time_filter = 'week'
    reddit_topic_top_limit = 5000
    topics = []
    mongo_client = None

    def __init__(self, topic='CryptoMoonShots'):
        self.reddit_instance = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent="Scrapper",
            username=os.getenv('REDDIT_USER_NAME'),
            password=os.getenv('REDDIT_PASSWORD'),
        )
        self.reddit_topic = topic
        self.sub_reddit_instance = self.reddit_instance.subreddit(self.reddit_topic)
        self.mongo_client = RedditScrapperMongo()

    def fetch_reddit_topics(self):
        """
        Fetch the reddit top topics
        """
        self.topics = self.sub_reddit_instance.top(
            time_filter=self.reddit_topic_time_filter,
            limit=self.reddit_topic_top_limit
        )

    def process_topics(self):
        """
        Find the crypto symbol from topics
        Format the data for crypto symbols
        Insert the data to mongo-db
        """
        for topic in self.topics:
            crypto_symbol_comments_mentioned_count = 0
            crypto_symbol, crypto_symbol_found_location = extract_crypto_symbol(topic.title), 'title'
            if not crypto_symbol:
                crypto_symbol, crypto_symbol_found_location = extract_crypto_symbol(topic.selftext), 'description'
            if crypto_symbol:
                print("========================================================================")
                setattr(topic, 'crypto_symbol', crypto_symbol)
                setattr(topic, 'created_at', convert_unix_timestamp_to_date_time(topic.created_utc))
                setattr(topic, 'symbol_found_location', crypto_symbol_found_location)
                print(topic.crypto_symbol)
                print(topic.created_at)
                print(topic.id)
                topic.comments.replace_more(limit=None)
                print("===> fetching comments")
                for comment in topic.comments.list():
                    if crypto_symbol.lower() in comment.body.lower():
                        crypto_symbol_comments_mentioned_count += 1
                setattr(topic, 'crypto_symbol_comments_mentioned_count', crypto_symbol_comments_mentioned_count)
                self.mongo_client.insert_topic(reddit_topic=topic)

    def run(self):
        self.fetch_reddit_topics()
        self.process_topics()
