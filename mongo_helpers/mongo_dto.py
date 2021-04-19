import os
import pymongo
from utils.helpers import convert_string_to_object_id


class RedditScrapperMongo(object):
    client = None
    database = None
    collection = None

    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv('MONGO_DB_HOST'), int(os.getenv('MONGO_DB_PORT')))
        self.database = self.client[os.getenv('MONGO_DATABASE_NAME')]
        self.collection = self.database[os.getenv('MONGO_COLLECTION_NAME')]

    def create_indexes(self):
        """
        Compound index for crypto_symbols collection
        """
        self.collection.create_index([
            ('crypto_symbol', pymongo.ASCENDING),
            ('created_at', pymongo.ASCENDING),
        ])

    def insert_topic(self, reddit_topic=None):
        """
        Insert an entry using upsert mechanism for mongo-db.
        """
        if reddit_topic:
            reddit_topic_id = convert_string_to_object_id(reddit_topic.id)
            self.collection.update_one(
                {'_id': reddit_topic_id},  # filters
                {
                    '$set': {
                        "_id": reddit_topic_id,
                        "crypto_symbol": reddit_topic.crypto_symbol,
                        "created_at": reddit_topic.created_at,
                        "topic_id": reddit_topic.id,
                        "url": reddit_topic.url,
                        "crypto_symbol_comments_mentioned_count": reddit_topic.crypto_symbol_comments_mentioned_count,
                        "symbol_found_location": reddit_topic.symbol_found_location
                    }
                },  # updates
                upsert=True
            )
            return True
        return False



