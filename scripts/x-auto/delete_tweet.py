import sys
import x_poster
import logging
import config

# ロギング設定
logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    if len(sys.argv) < 2:
        print("Usage: python delete_tweet.py <tweet_id>")
        sys.exit(1)

    tweet_id = sys.argv[1]
    print(f"Attempting to delete tweet ID: {tweet_id}")
    
    response = x_poster.delete_tweet(tweet_id)
    if response:
        print(f"Successfully deleted tweet {tweet_id}")
    else:
        print(f"Failed to delete tweet {tweet_id}. Check logs.")

if __name__ == "__main__":
    main()
