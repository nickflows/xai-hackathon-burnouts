import yaml
import requests
import json

def judge_political_leaning(post_content):
    with open('/Users/nicholasflores/Documents/Secrets/xai.yaml', 'r') as file:
        config = yaml.safe_load(file)
        xai_api_key = config['xai']['bearer']

    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {xai_api_key}"
    }
    data = {
        "messages": [
            {
                "role": "system",
                "content": """You are Grok, a chatbot that generates two-dimensional scores summarizing
                the political content of user-provided input. The two dimensions are:
                (1) Left-Right and (2) Libertarian-Authoritarian.
                Scores must range from 1 to 10. After generating the score,
                please generate a query to be used via the X API that would return recent
                relevant posts on the *opposite* end of the political spectrum."""
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
