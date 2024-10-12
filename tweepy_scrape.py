import tweepy
import datetime
from datetime import timedelta
import yaml
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load the bearer token from the yaml file
with open('/Users/nicholasflores/Documents/Secrets/xai.yaml', 'r') as file:
    config = yaml.safe_load(file)
    bearer_token = config['x']['bearer']

# Authenticate using the bearer token
client = tweepy.Client(bearer_token=bearer_token)

# Define the accounts you want to pull tweets from
accounts = ['nickflows', 'Andercot', '']  # Replace with Twitter handles

# Function to pull tweets for a single account
def get_tweets_for_account(account, since):
    tweets = []
    
    # Get user ID for the Twitter handle
    user = client.get_user(username=account)
    user_id = user.data.id

    # Pull the tweets from that user within the last 7 days
    response = client.get_users_tweets(
        user_id=user_id,
        start_time=since.isoformat() + 'Z',  # Twitter API requires ISO format with 'Z' as UTC timezone
        max_results=100,  # Max results per request (set lower if needed)
        tweet_fields=['created_at', 'text']  # Fetch only the relevant fields
    )

    if response.data:
        for tweet in response.data:
            tweets.append({
                'username': account,
                'created_at': tweet.created_at,
                'text': tweet.text
            })
    
    return tweets

# Function to pull tweets from multiple accounts
def get_tweets_from_accounts(accounts, since):
    all_tweets = []
    for account in accounts:
        tweets = get_tweets_for_account(account, since)
        all_tweets.extend(tweets)
    return all_tweets

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        accounts = request.form.get('accounts').split(',')
        days = int(request.form.get('days', 7))
        
        today = datetime.datetime.utcnow()
        since = today - timedelta(days=days)
        
        tweets = get_tweets_from_accounts(accounts, since)
        return jsonify(tweets)
    
    return render_template('template.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
