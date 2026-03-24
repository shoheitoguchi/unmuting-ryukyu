import anthropic
import config
import json
import os

client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

def generate_post(prompt, model="claude-sonnet-4-6"):
    """AIを使って投稿文を生成する"""
    try:
        response = client.messages.create(
            model=model,
            max_tokens=4000,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error generating post: {e}")
        return None

def generate_batch_posts(personality_profile, count=7):
    """
    一括で投稿を生成する（将来的に実装）
    personality_profile: account_profile.py の内容
    count: 生成する日数（1日3件計算なら count*3）
    """
    # ここにプロンプトのロジックを実装
    pass
