from openai import OpenAI
import base64
import io
import json
import os
from PIL import Image
import requests

class MemeExplainer(object):
    """
    Defines a class that explains meme images in a tweet. Initialize class with a config dictionary.
    """
    search_url_template = "https://api.x.com/2/tweets/{tweet_id}/?expansions=author_id,attachments.media_keys&media.fields=media_key,type,url"
    
    def __init__(self, config):
        self.bearer_token = config['bearer_token']
        self.xai_api_key = config['xai_api_key']

    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2FullArchiveSearchPython"
        return r

    def connect_to_endpoint(self, url, params):
        response = requests.request("GET", url, auth=self.bearer_oauth, params=params)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        self.json_response = response.json()
        return

    def format_template(self, tweet_id):
        self.search_url = self.search_url_template.format(tweet_id=tweet_id)
        return

    def get_image_url(self, tweet_id):
        self.format_template(tweet_id)
        self.connect_to_endpoint(url=self.search_url, params=None)
        self.image_url = self.json_response["includes"]["media"][0]["url"]
        return

    def encode_image_url(self):
        image_url = self.image_url
        response = requests.get(image_url)
        with Image.open(io.BytesIO(response.content)) as img:
            image = img.convert("RGB")
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="JPEG", quality=95)
        image_bytes = img_byte_arr.getvalue()
        self.base64_image = base64.b64encode(image_bytes).decode("utf-8")
        return self.base64_image

    def explain(self, tweet_id):

        self.get_image_url(tweet_id)
        base64_image = self.encode_image_url()  # Getting the base64 string

        messages = [
           {
               "role": "user",
               "content": [
                   {
                       "type": "image_url",
                       "image_url": {
                           "url": f"data:image/jpeg;base64,{self.base64_image}",
                           "detail": "high",
                       },
                   },
                   {
                       "type": "text",
                       "text": "Explain this meme. Then rate it on the following scale: {1: TOTALLY BASED, 2: BASED, 3: MID, 4: BIASED, 5: HELLA BIASED}",
                   },
               ],
           },
        ]
        client = OpenAI(
           base_url="https://api.x.ai/v1",
           api_key=os.getenv("XAI_API_KEY_V2", self.xai_api_key),
        )
        stream = client.chat.completions.create(
           model="grok-vision-preview",
           messages=messages,
           stream=True,
           temperature=0.01,
        )
        for chunk in stream:
            print(chunk.choices[0].delta.content, end="", flush=True)
        print("\n\n")
