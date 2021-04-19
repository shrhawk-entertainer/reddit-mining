from dotenv import load_dotenv
from reddit_scrapper.scrapper import RedditScrapper

load_dotenv()

if __name__ == "__main__":
    RedditScrapper().run()
