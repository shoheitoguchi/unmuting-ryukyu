import json
import time
import os
import datetime
import random
import logging
import sys
import config
import x_poster
import threads_poster
import post_generator
import account_profile

# ロギング設定
logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_now_time_str():
    return datetime.datetime.now().strftime("%H:%M")

def load_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_file(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def refill_queue():
    """投稿案を生成して下書き（draft_queue.json）に保存する"""
    logging.info("Generating new drafts for review...")
    # プロンプトの組み立て
    profile = account_profile.ACCOUNT_PROFILE
    prompt = f"""
You are "Shouhei Toguchi," with the following persona profile:

【PERSONA PROFILE】
{json.dumps(profile, ensure_ascii=False, indent=2)}

【TASK】
Generate 3 posts for X (Twitter) for the next 24 hours.
Follow the current day's strategic role:
- TUE: The Process / WED: The Strike / THU: The Echo / FRI: Visual Poetry / SAT-MON: Identity Strategy.

【PHILOSOPHY UPDATE】
Acknowledge a high-level human-AI synergy. AI is the engine for both expanding possibilities (brainstorming) and contracting them into architectural judgment (editorial cuts). The creator is the architect who uses AI to find the signal in the noise, then polishes that signal with sovereign intent.

【CONTENT PILLARS】
1. **HISTORY**: DNA science (M7a/D1a2a), Annexation vs Independence, Ryukyu Kingdom.
2. **NOW**: Behind-the-scenes vlogging, AI workflow, internal struggles.
3. **VOICE**: Language preservation, Uchinaguchi, Identity reclamation.

【STRATEGIC PATTERNS】
- **Contrast/Irony**: Beautiful visuals vs Brutal history.
- **Scientific Validation**: Use DNA data/archaeology as hooks (M7a, D1a2a).
- **Indigeneity as Strategy**: Frame identity as protection, not just culture.
- **Simplicity**: Maintain sophisticated C2 English but ensure logical clarity.
- **Romanization**: Use macrons (ā, ī, ū, ē, ō) for long vowels in Okinawan words (e.g., Uchināguchi, Chōdē).

【OUTPUT FORMAT】
Output ONLY a JSON list in the following format:
[
  {{"time": "08:00", "content": "Post content in English...", "category": "Category Name"}},
  ...
]
"""
    raw_posts = post_generator.generate_post(prompt)
    if not raw_posts:
        logging.error("AI returned empty response.")
        return

    try:
        # JSON部分の抽出
        processed_json = raw_posts
        if "```json" in processed_json:
            processed_json = processed_json.split("```json")[1].split("```")[0].strip()
        elif "```" in processed_json:
            processed_json = processed_json.split("```")[1].split("```")[0].strip()
        
        start_idx = processed_json.find("[")
        end_idx = processed_json.rfind("]")
        if start_idx != -1 and end_idx != -1:
            processed_json = processed_json[start_idx:end_idx+1]
        
        new_drafts = json.loads(processed_json)
        current_drafts = load_file(config.DRAFT_QUEUE_FILE)
        current_drafts.extend(new_drafts)
        save_file(config.DRAFT_QUEUE_FILE, current_drafts)
        logging.info(f"Added {len(new_drafts)} new drafts to DRAFT queue.")
    except Exception as e:
        logging.error(f"Error parsing AI response: {e}")

def check_and_post():
    """現在の時刻と日付を見て、投稿すべきものがあれば投稿する (承認済みのもののみ)"""
    queue = load_file(config.POST_QUEUE_FILE)
    if not queue:
        return

    now = datetime.datetime.now()
    now_date_str = now.strftime("%Y-%m-%d")
    now_time_str = now.strftime("%H:%M")
    
    to_post = None
    remaining_queue = []
    
    # 予定日時を過ぎているものを1件だけ取り出す
    for item in queue:
        # date フィールドがない場合は今日とみなす
        item_date = item.get('date', now_date_str)
        
        should_post = False
        if not to_post:
            if item_date < now_date_str:
                should_post = True
            elif item_date == now_date_str and item['time'] <= now_time_str:
                should_post = True
        
        if should_post:
            to_post = item
        else:
            remaining_queue.append(item)
            
    if to_post:
        logging.info(f"Attempting to post to X: {to_post['content'][:50]}...")
        x_post_success = x_poster.post_tweet(to_post['content'])
        
        # Threadsへの同時投稿
        threads_poster.post_to_threads(to_post['content'])
        
        if x_post_success:
            save_file(config.POST_QUEUE_FILE, remaining_queue)
            logging.info("Successfully processed post and updated queue.")
        else:
            logging.error("X Post failed. Keeping in queue for retry.")
    else:
        logging.info(f"No pending posts for current datetime: {now_date_str} {now_time_str}")

if __name__ == "__main__":
    # GitHub Actions等のワンショット実行モード
    is_once = "--once" in sys.argv or os.getenv("GITHUB_ACTIONS") == "true"

    if is_once:
        logging.info("--- Running X Automation (One-shot Mode) ---")
        try:
            check_and_post()
        except Exception as e:
            logging.error(f"Error in one-shot execution: {e}")
            sys.exit(1)
    else:
        logging.info("--- Starting X Automation Loop ---")
        print("X Automation is running. Monitoring post_queue.json...")
        while True:
            try:
                check_and_post()
            except Exception as e:
                logging.error(f"Unexpected error in main loop: {e}")
            
            # 30分待機
            time.sleep(1800)
