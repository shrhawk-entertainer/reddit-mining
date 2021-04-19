import re
from datetime import datetime
from bson import ObjectId


def convert_unix_timestamp_to_date_time(unix_timestamp: int):
    """
    Convert unix timestamp to python datetime object
    :param unix_timestamp:
    :return: datetime
    """
    return datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')


def extract_crypto_symbol(text: str = ''):
    """
    Extract the crypto symbol from string in the format of $WORD example $DEMO, $DEMO1
    if crypto symbol contains only digits example $1500 then it will not consider as crypto symbol.
    :param text:
    :return:
    """
    crypto_symbols = re.findall('\$([\w]+)', text)
    if crypto_symbols:
        for symbol in crypto_symbols:
            if not symbol.isdigit():
                return symbol
    return None


def convert_string_to_object_id(text: str = '') -> ObjectId:
    """
    Convert python str to mongodb ObjectId
    """
    return ObjectId(text.ljust(12, "r").encode())
