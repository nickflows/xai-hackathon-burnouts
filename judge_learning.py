import yaml
import requests
import json
import logging

def judge_political_leaning(post_content):
    try:
        with open('/Users/nicholasflores/Documents/Secrets/xai.yaml', 'r') as file:
            config = yaml.safe_load(file)
            xai_api_key = config['xai']['bearer']
    except Exception as e:
        logging.error(f"Error loading XAI API key: {str(e)}")
        return "Error: Unable to load XAI API key"

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
                please generate a structured list of keywords to be used to query the X API
                that would return recent relevant posts on the *opposite* end of the political spectrum."""
            },
            {
                "role": "user",
                "content": post_content
            }
        ],
        "model": "grok-preview",
        "stream": False,
        "temperature": 0
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # This will raise an exception for HTTP errors
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling XAI API: {str(e)}")
        return f"Error: Unable to get analysis from XAI API"
