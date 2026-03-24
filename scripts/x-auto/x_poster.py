import tweepy
import config
import logging

# ロギング設定
logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_client():
    """X API v2 クライアントを取得"""
    return tweepy.Client(
        consumer_key=config.X_API_KEY,
        consumer_secret=config.X_API_KEY_SECRET,
        access_token=config.X_ACCESS_TOKEN,
        access_token_secret=config.X_ACCESS_TOKEN_SECRET
    )

def post_tweet(text):
    """ツイートを投稿する"""
    try:
        client = get_client()
        response = client.create_tweet(text=text)
        logging.info(f"Successfully posted: {response.data['id']}")
        return response
    except Exception as e:
        logging.error(f"Error posting tweet: {e}")
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # テスト投稿用
    test_text = "Testing X Automation System from Ryukyu."
    # post_tweet(test_text) # 全てのキーが揃ったらコメントアウトを外す
    print("X Poster module loaded.")
