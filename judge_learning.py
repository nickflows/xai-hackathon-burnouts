import requests
import json

def judge_political_leaning(post_content):
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_XAI_API_KEY"  # Replace with your actual API key
    }
    data = {
        "messages": [
            {
                "role": "system",
                "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."
            },
            {
                "role": "user",
                "content": post_content
            }
        ],
        "model": "grok-2-mini-public",
        "stream": False,
        "temperature": 0
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"
