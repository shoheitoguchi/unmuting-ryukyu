import requests
import config
import logging

def post_to_threads(text):
    """Threads に投稿する (Meta Graph API)"""
    if not config.THREADS_ACCESS_TOKEN or not config.THREADS_USER_ID:
        logging.warning("Threads API credentials not set. Skipping Threads post.")
        return None

    # 第一ステップ: メディアコンテナの作成
    # https://developers.facebook.com/docs/threads/threads-api/threads-posts
    url = f"https://graph.threads.net/v1.0/{config.THREADS_USER_ID}/threads"
    params = {
        "media_type": "TEXT",
        "text": text,
        "access_token": config.THREADS_ACCESS_TOKEN
    }
    
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        container_id = response.json().get("id")
        
        # 第二ステップ: メディアの公開
        publish_url = f"https://graph.threads.net/v1.0/{config.THREADS_USER_ID}/threads_publish"
        publish_params = {
            "creation_id": container_id,
            "access_token": config.THREADS_ACCESS_TOKEN
        }
        publish_response = requests.post(publish_url, publish_params=publish_params)
        publish_response.raise_for_status()
        
        logging.info(f"Successfully posted to Threads: {publish_response.json()}")
        return publish_response.json()
    except Exception as e:
        logging.error(f"Error posting to Threads: {e}")
        print(f"Threads Error: {e}")
        return None
