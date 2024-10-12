import tweepy
import datetime
from datetime import timedelta
import yaml
from flask import Flask, render_template, request, jsonify
from collections import defaultdict
from judge_learning import judge_political_leaning
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load the bearer token from the yaml file
try:
    with open('/Users/nicholasflores/Documents/Secrets/xai.yaml', 'r') as file:
        config = yaml.safe_load(file)
        bearer_token = config['x']['bearer']
except Exception as e:
    logging.error(f"Error loading config: {str(e)}")
    raise

# Authenticate using the bearer token
try:
    client = tweepy.Client(bearer_token=bearer_token)
except Exception as e:
    logging.error(f"Error authenticating with Twitter: {str(e)}")
    raise

# Define the accounts you want to pull tweets from
accounts = ['nickflows', 'Andercot', '']  # Replace with Twitter handles

# Function to pull tweets for a single account
def get_tweets_for_account(account, since):
    tweets = []
    
    try:
        # Get user ID for the Twitter handle
        user = client.get_user(username=account)
        user_id = user.data.id

        # Format the start_time correctly
        start_time = since.strftime('%Y-%m-%dT%H:%M:%SZ')

        # Pull the tweets from that user within the specified time range
        response = client.get_users_tweets(
            id=user_id,
            start_time=start_time,
            max_results=100,
            tweet_fields=['created_at', 'text']
        )

        if response.data:
            for tweet in response.data:
                try:
                    ai_analysis = judge_political_leaning(tweet.text)
                    tweets.append({
                        'username': account,
                        'created_at': tweet.created_at,
                        'text': tweet.text,
                        'ai_score': ai_analysis
                    })
                except Exception as e:
                    logging.error(f"Error analyzing tweet: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching tweets for {account}: {str(e)}")
    
    return tweets

# Function to pull tweets from multiple accounts
def get_tweets_from_accounts(accounts, since):
    all_tweets = []
    for account in accounts:
        tweets = get_tweets_for_account(account, since)
        all_tweets.extend(tweets)
    return all_tweets

@app.route('/')
def home():
    return render_template('xaiHackHome.html')

@app.route('/demo1', methods=['GET', 'POST'])
def demo1():
    if request.method == 'POST':
        try:
            accounts = request.form.get('accounts').split(',')
            days = int(request.form.get('days', 7))
            
            today = datetime.datetime.utcnow()
            since = today - timedelta(days=days)
            
            # Ensure we're not using a future date
            since = min(since, today)
            
            tweets = get_tweets_from_accounts(accounts, since)
            
            # Organize tweets by user
            tweets_by_user = defaultdict(list)
            for tweet in tweets:
                tweets_by_user[tweet['username']].append(tweet)
            
            return jsonify(dict(tweets_by_user))
        except Exception as e:
            logging.error(f"Error in demo1 route: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    return render_template('template.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
